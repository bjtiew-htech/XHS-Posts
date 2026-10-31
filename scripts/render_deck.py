#!/usr/bin/env python3
"""
渲染：posts/YYMMDD-XX/index.html 的每个 .poster → 01.jpg..NN.jpg（1080×1440，JPEG q95），
清理多余旧图，并写 .render_manifest.json（记录渲染时 index.html 的 sha256）。
preflight 用 manifest 的哈希判断图片是否最新，不再依赖文件修改时间（IDE 自动保存不会误判）。

用法：python3 scripts/render_deck.py posts/261031-01 [posts/... ...]
"""
import datetime
import json
import os
import shutil
import subprocess
import sys

from PIL import Image

from common import RENDER_MJS, REPO_ROOT, load_rules, sha256_file, slide_images


def render_post(post_dir: str) -> None:
    rules = load_rules()
    W, H = rules["slides"]["width"], rules["slides"]["height"]
    post_dir = os.path.abspath(post_dir)
    html_path = os.path.join(post_dir, "index.html")
    if not os.path.exists(html_path):
        raise FileNotFoundError(f"Missing index.html in {post_dir}")

    html_hash = sha256_file(html_path)
    out_tmp = os.path.join(post_dir, "_render_tmp")
    shutil.rmtree(out_tmp, ignore_errors=True)
    res = subprocess.run(
        ["node", RENDER_MJS, html_path, "--out", out_tmp],
        check=True, cwd=REPO_ROOT, capture_output=True, text=True,
    )
    pngs = json.loads(res.stdout.strip().splitlines()[-1])["files"]
    if not pngs:
        raise RuntimeError(f"No .poster rendered in {html_path}")

    for idx, png in enumerate(pngs, start=1):
        with Image.open(png) as im:
            rgb = im.convert("RGB")
            if rgb.size != (W, H):
                raise RuntimeError(f"{png} size {rgb.size} != ({W}, {H})")
            rgb.save(os.path.join(post_dir, f"{idx:02d}.jpg"), "JPEG", quality=95, optimize=True)
    shutil.rmtree(out_tmp, ignore_errors=True)

    for jpg in slide_images(post_dir):
        if int(os.path.basename(jpg)[:2]) > len(pngs):
            os.remove(jpg)
            print(f"  [cleanup] removed stale {os.path.basename(jpg)}")

    if sha256_file(html_path) != html_hash:
        raise RuntimeError("index.html changed during render — re-run render_deck.py")

    manifest = {
        "index_html_sha256": html_hash,
        "slide_count": len(pngs),
        "images": {os.path.basename(p): sha256_file(p) for p in slide_images(post_dir)},
        "rendered_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    with open(os.path.join(post_dir, ".render_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"[Render] {os.path.basename(post_dir)}: {len(pngs)} cards → 01.jpg..{len(pngs):02d}.jpg")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    for target in sys.argv[1:]:
        render_post(target)
