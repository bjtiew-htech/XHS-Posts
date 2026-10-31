#!/usr/bin/env python3
"""
数据回流：录入发布后数据，并按 experiments/sprint_XX.md 预注册的规则判定 A/B 结果。

录入（追加到 tracker/metrics_snapshots.csv）：
  python3 scripts/log_metrics.py add 261031-01 --impressions 820 --views 131 \
      [--likes 3 --comments 2 --saves 5 --shares 1 --avg-view-sec 41 --followers 1] [--checkpoint T48h]

判定（读取 posts_master.csv 的 ab_sprint / ab_pair_id / variant + 每帖 T48h 快照）：
  python3 scripts/log_metrics.py evaluate Sprint1_Cover_Test
"""
import argparse
import csv
import datetime
import math
import os
import sys

from common import REPO_ROOT

SNAP = os.path.join(REPO_ROOT, "tracker", "metrics_snapshots.csv")
MASTER = os.path.join(REPO_ROOT, "tracker", "posts_master.csv")
MIN_IMPRESSIONS = 200       # 预注册：低于此值视为疑似限流，整对剔除
MIN_PAIRS_SAME_DIR = 4      # 预注册：6 对中至少 4 对方向一致
ALPHA = 0.05


def read_csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def add(a):
    master = {r["post_id"]: r for r in read_csv(MASTER)}
    if a.post_id not in master:
        sys.exit(f"{a.post_id} not in posts_master.csv")
    pub = datetime.date.fromisoformat(master[a.post_id]["publish_date"])
    today = datetime.date.today()
    age = max((today - pub).days, 1)
    ctr = round(100 * a.views / a.impressions, 2) if a.impressions else 0.0
    inter = a.likes + a.comments + a.saves + a.shares
    rows = read_csv(SNAP)
    prev = [r for r in rows if r["post_id"] == a.post_id]
    delta = a.impressions - (int(prev[-1]["impressions"]) if prev else 0)
    row = {
        "snapshot_date": today.isoformat(), "post_id": a.post_id, "publish_date": pub.isoformat(),
        "age_days": age, "checkpoint_type": a.checkpoint, "impressions": a.impressions, "views": a.views,
        "cover_ctr_pct": ctr, "interaction_rate_pct": round(100 * inter / a.views, 2) if a.views else 0.0,
        "likes": a.likes, "comments": a.comments, "saves": a.saves, "shares": a.shares,
        "avg_view_sec": a.avg_view_sec, "new_followers": a.followers,
        "delta_impressions": delta, "velocity_imp_per_day": round(a.impressions / age, 1),
    }
    with open(SNAP, encoding="utf-8") as f:
        header = next(csv.reader(f))
    with open(SNAP, "a", encoding="utf-8", newline="") as f:
        csv.DictWriter(f, fieldnames=header).writerow({k: row.get(k, "") for k in header})
    print(f"[metrics] {a.post_id} {a.checkpoint}: 曝光 {a.impressions} 观看 {a.views} 封面CTR {ctr}%")


def evaluate(a):
    master = [r for r in read_csv(MASTER) if r["ab_sprint"] == a.sprint]
    snaps = {}
    for r in read_csv(SNAP):
        if r["checkpoint_type"] == "T48h":
            snaps[r["post_id"]] = r
    pairs = {}
    for r in master:
        pairs.setdefault(r["ab_pair_id"], {})[r["variant"]] = r["post_id"]

    tot = {}
    wins = {}
    print(f"== {a.sprint} ==")
    for pid, var in sorted(pairs.items()):
        if len(var) != 2 or not all(p in snaps for p in var.values()):
            print(f"  {pid}: 数据不全，跳过 {var}")
            continue
        s = {v: snaps[p] for v, p in var.items()}
        if any(int(x["impressions"]) < MIN_IMPRESSIONS for x in s.values()):
            print(f"  {pid}: 曝光 < {MIN_IMPRESSIONS}（疑似限流），按预注册规则剔除")
            continue
        ctr = {v: int(x["views"]) / int(x["impressions"]) for v, x in s.items()}
        for v, x in s.items():
            t = tot.setdefault(v, [0, 0])
            t[0] += int(x["impressions"])
            t[1] += int(x["views"])
        w = max(ctr, key=ctr.get)
        wins[w] = wins.get(w, 0) + 1
        print(f"  {pid}: " + "  ".join(f"{v} {100 * c:.1f}%" for v, c in ctr.items()) + f"  → {w}")

    if len(tot) != 2:
        print("有效对不足，无法判定。")
        return
    (va, (na, xa)), (vb, (nb, xb)) = sorted(tot.items())
    pa, pb = xa / na, xb / nb
    p = (xa + xb) / (na + nb)
    se = math.sqrt(p * (1 - p) * (1 / na + 1 / nb))
    z = (pa - pb) / se if se else 0.0
    pval = math.erfc(abs(z) / math.sqrt(2))
    leader = va if pa > pb else vb
    print(f"\n  汇总：{va} {100 * pa:.2f}%（{xa}/{na}）  vs  {vb} {100 * pb:.2f}%（{xb}/{nb}）  z={z:.2f}  p={pval:.3f}")
    print(f"  逐对胜出：{wins}")
    if pval < ALPHA and wins.get(leader, 0) >= MIN_PAIRS_SAME_DIR:
        print(f"  结论：{leader} 胜出（p<{ALPHA} 且 ≥{MIN_PAIRS_SAME_DIR} 对方向一致）→ 写入 config/brand.md 作为新基线")
    else:
        print("  结论：无显著差异 → 保留 Cover_B_Typography 为默认，Sprint 2 换测下一个变量")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    ad = sub.add_parser("add")
    ad.add_argument("post_id")
    ad.add_argument("--impressions", type=int, required=True)
    ad.add_argument("--views", type=int, required=True)
    for k in ["likes", "comments", "saves", "shares", "followers"]:
        ad.add_argument(f"--{k}", type=int, default=0)
    ad.add_argument("--avg-view-sec", type=float, default=0.0)
    ad.add_argument("--checkpoint", default="T48h")
    ev = sub.add_parser("evaluate")
    ev.add_argument("sprint")
    args = ap.parse_args()
    add(args) if args.cmd == "add" else evaluate(args)

