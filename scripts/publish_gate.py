#!/usr/bin/env python3
"""
机器闸门 #2（publish）：放行条件全部满足才允许发布。

1. 交付物齐全（config/rules.json → required_files.publish）
2. 04_preflight_report.json 为 PASS，且其 content_hash == 当前内容哈希
3. critic_audit.md 里的 conversation://<uuid> 指向一个真实存在的独立 critic 对话；
   publish_gate 直接读取该对话的原始 transcript（而不是相信 critic_audit.md 的转写），
   要求 critic 对“当前内容哈希”的最后一次结论是 VERDICT: APPROVED。
   → 审核之后改动 text.md / index.html / 任一 jpg，哈希改变，批准自动作废。

用法：python3 scripts/publish_gate.py posts/261031-01 [posts/... ...]
"""
import json
import os
import re
import sys

from common import content_hash, load_rules

UUID = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"


def critic_verdicts(conv_id: str, R: dict) -> list[tuple[str, str]]:
    """返回 critic 对话中按时间顺序出现的 (verdict, audited_hash)。只读取 MODEL 产出的步骤。"""
    root = os.path.expanduser(R["critic"]["transcript_root"])
    rel = R["critic"]["transcript_relpath"]
    path = os.path.join(root, conv_id, rel.replace("transcript.jsonl", "transcript_full.jsonl"))
    if not os.path.exists(path):
        path = os.path.join(root, conv_id, rel)
    if not os.path.exists(path):
        raise FileNotFoundError(f"critic transcript not found for conversation {conv_id}")
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            step = json.loads(line)
            if step.get("source") != "MODEL" or step.get("type") != "PLANNER_RESPONSE":
                continue
            blob = (step.get("content") or "") + json.dumps(step.get("tool_calls") or [], ensure_ascii=False)
            blob = blob.replace("\\n", "\n")
            for m in re.finditer(r"VERDICT:\s*(APPROVED|VETO_REJECT)[\s\S]{0,400}?AUDITED_HASH:\s*([0-9a-f]{16})", blob):
                out.append((m.group(1), m.group(2)))
    return out


def verify_release(post_dir: str) -> bool:
    R = load_rules()
    post_dir = os.path.abspath(post_dir)
    post_id = os.path.basename(post_dir)
    errs = [f"missing {f}" for f in R["required_files"]["publish"] if not os.path.exists(os.path.join(post_dir, f))]
    if errs:
        print(f"[Publish] {post_id}: ❌ BLOCKED {errs}")
        return False

    now_hash = content_hash(post_dir)
    pf = json.load(open(os.path.join(post_dir, "04_preflight_report.json"), encoding="utf-8"))
    if pf.get("status") != "PASS":
        errs.append(f"preflight status = {pf.get('status')}")
    if pf.get("content_hash") != now_hash:
        errs.append(f"content changed after preflight ({pf.get('content_hash')} → {now_hash}); re-run render + preflight")

    audit = open(os.path.join(post_dir, "critic_audit.md"), encoding="utf-8").read()
    ids = re.findall(rf"conversation://({UUID})", audit)
    if not ids:
        errs.append("critic_audit.md has no conversation://<uuid>")
    else:
        try:
            verdicts = [v for cid in dict.fromkeys(ids) for v in critic_verdicts(cid, R)]
            mine = [v for v, h in verdicts if h == now_hash]
            if not mine:
                errs.append(f"no critic verdict found for current content hash {now_hash} (content changed after audit, or critic never audited this version)")
            elif mine[-1] != "APPROVED":
                errs.append(f"latest critic verdict for {now_hash} is {mine[-1]}")
        except FileNotFoundError as e:
            errs.append(str(e))

    if errs:
        print(f"[Publish] {post_id}: ❌ BLOCKED")
        for e in errs:
            print(f"   - {e}")
        return False
    print(f"[Publish] {post_id}: ✅ CLEARED ({pf.get('slide_count')} slides, hash {now_hash} approved by independent critic)")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    ok = all([verify_release(t) for t in sys.argv[1:]])
    sys.exit(0 if ok else 1)
