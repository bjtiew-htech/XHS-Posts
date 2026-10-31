"""共享工具：读取 config/rules.json、计算帖子内容哈希。所有 gate 脚本只从这里取规则。"""
import glob
import hashlib
import json
import os
import re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RENDER_MJS = os.path.join(REPO_ROOT, "tools", "render.mjs")


def load_rules() -> dict:
    with open(os.path.join(REPO_ROOT, "config", "rules.json"), "r", encoding="utf-8") as f:
        return json.load(f)


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def slide_images(post_dir: str) -> list[str]:
    return sorted(
        p for p in glob.glob(os.path.join(post_dir, "[0-9][0-9].jpg"))
        if re.fullmatch(r"\d{2}\.jpg", os.path.basename(p))
    )


def content_hash(post_dir: str) -> str:
    """审核绑定哈希：text.md + index.html + 全部 NN.jpg。任何一个变动，哈希即变，批准自动作废。"""
    h = hashlib.sha256()
    parts = [os.path.join(post_dir, "text.md"), os.path.join(post_dir, "index.html")] + slide_images(post_dir)
    for p in parts:
        h.update(os.path.basename(p).encode())
        h.update(sha256_file(p).encode() if os.path.exists(p) else b"MISSING")
    return h.hexdigest()[:16]
