#!/usr/bin/env python3
"""
机器闸门 #1（preflight）：确定性检查，任何一项 FAIL 都不得送独立审核。
规则全部来自 config/rules.json。输出 04_preflight_report.json，并打印本帖 content hash
（送审时必须把这个哈希交给 critic，critic 在结论里回写 AUDITED_HASH）。

检查项：上游交付物 / 标题长度 / 违禁与限流词 / 装饰英文 / 页数 / 页码 /
渲染新鲜度（manifest 哈希）/ 图片尺寸 / DOM 溢出 / text.md 必备段落 / QS 排名溯源到 02_fact_sheet.md

用法：python3 scripts/preflight_gate.py posts/261031-01 [posts/... ...]
"""
import datetime
import json
import os
import re
import subprocess
import sys

from bs4 import BeautifulSoup
from PIL import Image

from common import RENDER_MJS, REPO_ROOT, content_hash, load_rules, sha256_file, slide_images

QS_IN_POST = re.compile(r"QS\s*[`（(]?\s*(?:世界第\s*)?[#=]{0,2}\s*(\d{1,4})(?:\s*[–-]\s*(\d{1,4}))?")
RANK_IN_FACTS = re.compile(r"(?:#|QS\s*[`（(]?\s*(?:世界第\s*)?=?#?)\s*=?(\d{1,4})")


def dom_geometry(html_path: str) -> list[dict]:
    res = subprocess.run(["node", RENDER_MJS, html_path, "--check-only"],
                         check=True, cwd=REPO_ROOT, capture_output=True, text=True)
    return json.loads(res.stdout.strip().splitlines()[-1])["posters"]


def audit_post(post_dir: str) -> bool:
    R = load_rules()
    post_dir = os.path.abspath(post_dir)
    post_id = os.path.basename(post_dir)
    errors, checks = [], {}

    def record(name: str, errs: list[str], ok_note: str = "PASS") -> None:
        checks[name] = ok_note if not errs else f"FAIL: {errs}"
        errors.extend(errs)

    # 1. 上游交付物
    missing = [f for f in R["required_files"]["preflight"]
               if not os.path.exists(os.path.join(post_dir, f)) or os.path.getsize(os.path.join(post_dir, f)) < 100]
    record("upstream_deliverables", [f"missing/empty {m}" for m in missing])
    text_path, html_path = os.path.join(post_dir, "text.md"), os.path.join(post_dir, "index.html")
    if not (os.path.exists(text_path) and os.path.exists(html_path)):
        print(f"[Preflight] {post_id}: FAIL (missing text.md / index.html)")
        return False

    text_md = open(text_path, encoding="utf-8").read()
    raw_html = open(html_path, encoding="utf-8").read()
    vis = BeautifulSoup(raw_html, "html.parser")
    for tag in vis(["style", "script"]):
        tag.decompose()
    visible = vis.get_text(" ", strip=True)
    combined = text_md + "\n" + visible

    # 2. 标题
    m = re.search(r"1\.\s*\*\*([^*]+)\*\*\s*\*\(Selected", text_md)
    if not m:
        record("title_length", ["text.md missing '1. **<TITLE>** *(Selected...)*'"])
    else:
        t = m.group(1).strip()
        bad = len(t) > R["title"]["max_chars"] or R["title"]["required_separator"] not in t
        record("title_length", [f"title '{t}' len={len(t)}"] if bad else [], f"PASS ({len(t)} chars): {t}")

    # 3. 违禁 / 限流词 + 禁诱导留言换奖励
    words = R["banned_words"]["absolute"] + R["banned_words"]["throttle"]
    hits = [f"text.md contains '{w}'" for w in words if w in text_md] + \
           [f"index.html contains '{w}'" for w in words if w in visible]
    # Check comment inducement patterns on Body/Hashtag/Pinned Comment and visible HTML
    public_text_md = text_md.split("### 💬 Blue-V Comment Follow-Up Script")[0]
    for pat in R.get("comment_inducement_patterns", []):
        if re.search(pat, public_text_md):
            hits.append(f"text.md matches comment inducement pattern '{pat}'")
        if re.search(pat, visible):
            hits.append(f"index.html matches comment inducement pattern '{pat}'")
    record("banned_words", hits)

    # 3b. 正文 + Hashtag 总字数上限（Hashtag 计入字数）
    max_body_chars = R.get("body_plus_hashtags_max_chars", 1000)
    m_body = re.search(r"###\s*Body:\s*\n([\s\S]*?)\n---\s*\n###\s*Hashtag:\s*\n([\s\S]*?)(?:\n---|\Z)", text_md)
    if not m_body:
        record("body_plus_hashtags_length", ["cannot parse ### Body: and ### Hashtag: sections in text.md"])
    else:
        body_part = m_body.group(1).strip()
        hashtag_part = m_body.group(2).strip()
        combined_post_text = f"{body_part}\n\n{hashtag_part}"
        total_len = len(combined_post_text)
        record(
            "body_plus_hashtags_length",
            [f"Body + Hashtags len={total_len} exceeds max {max_body_chars}"] if total_len > max_body_chars else [],
            f"PASS ({total_len}/{max_body_chars} chars incl. hashtags)"
        )

    # 4. 装饰英文
    record("zero_decorative_english",
           [f"decorative English: {p}" for p in R["decorative_english_patterns"] if re.search(p, visible)])

    # 5. 页数 + 页码
    posters = BeautifulSoup(raw_html, "html.parser").select(".poster")
    n = len(posters)
    lo, hi = R["slides"]["min"], R["slides"]["max"]
    record("slide_count", [] if lo <= n <= hi else [f"{n} slides outside [{lo}..{hi}]"], f"PASS ({n} slides)")
    pag = []
    for idx, p in enumerate(posters, start=1):
        for mp in re.finditer(r"\b(\d{2})\s*/\s*(\d{2})\b", p.get_text(" ", strip=True)):
            if int(mp.group(1)) != idx or int(mp.group(2)) != n:
                pag.append(f"slide {idx:02d} shows '{mp.group(0)}' (expected {idx:02d} / {n:02d})")
    record("pagination_consistency", pag)

    # 6. 渲染新鲜度（哈希，不看 mtime）+ 尺寸
    W, H = R["slides"]["width"], R["slides"]["height"]
    img_errs = []
    man_path = os.path.join(post_dir, ".render_manifest.json")
    imgs = slide_images(post_dir)
    if not os.path.exists(man_path):
        img_errs.append("missing .render_manifest.json — run scripts/render_deck.py")
    else:
        man = json.load(open(man_path, encoding="utf-8"))
        if man.get("index_html_sha256") != sha256_file(html_path):
            img_errs.append("index.html content changed since last render — re-run render_deck.py")
        for p in imgs:
            if man.get("images", {}).get(os.path.basename(p)) != sha256_file(p):
                img_errs.append(f"{os.path.basename(p)} not produced by last render")
    if len(imgs) != n:
        img_errs.append(f"{len(imgs)} jpgs on disk vs {n} posters")
    for p in imgs:
        with Image.open(p) as im:
            if im.size != (W, H):
                img_errs.append(f"{os.path.basename(p)} size {im.size}")
    record("render_freshness_and_dimensions", img_errs)

    # 7. DOM 溢出
    tol = R["slides"]["overflow_tolerance_px"]
    dom = []
    for g in dom_geometry(html_path):
        if (g["width"], g["height"]) != (W, H):
            dom.append(f"{g['id']} box {g['width']}x{g['height']}")
        if g["scrollHeight"] > H + tol:
            dom.append(f"{g['id']} vertical overflow {g['scrollHeight']}")
        if g["scrollWidth"] > W + tol:
            dom.append(f"{g['id']} horizontal overflow {g['scrollWidth']}")
    record("chromium_dom_geometry", dom)

    # 8. text.md 必备段落
    record("text_md_sections",
           [f"text.md missing '{s}'" for s in R["text_md_required_sections"] if s not in text_md])

    # 9. QS 排名溯源：正文每个 QS 数字必须出现在 02_fact_sheet.md
    trace = []
    fs_path = os.path.join(post_dir, "02_fact_sheet.md")
    if R["fact_traceability"]["enforce_qs_ranks"] and os.path.exists(fs_path):
        fact_ranks = set(RANK_IN_FACTS.findall(open(fs_path, encoding="utf-8").read()))
        post_ranks = {g for mt in QS_IN_POST.finditer(combined) for g in mt.groups() if g}
        trace = [f"QS {r} cited in post but not found in 02_fact_sheet.md" for r in sorted(post_ranks - fact_ranks, key=int)]
    record("qs_rank_traceability", trace)

    status = "PASS" if not errors else "FAIL"
    chash = content_hash(post_dir)
    report = {
        "post_id": post_id,
        "gate": "preflight_gate.py (machine gate #1)",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "slide_count": n,
        "status": status,
        "content_hash": chash,
        "checks": checks,
        "errors": errors,
    }
    with open(os.path.join(post_dir, "04_preflight_report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"[Preflight] {post_id}: {status} ({n} slides) content_hash={chash}")
    for e in errors:
        print(f"   ❌ {e}")
    return status == "PASS"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    ok = all([audit_post(p) for p in sys.argv[1:]])
    sys.exit(0 if ok else 1)
