#!/usr/bin/env python3
"""
Exports each `.slide` element in a `slides.html` file into individual 1080x1440 (3:4 Retina) JPEG files (`01.jpg`, `02.jpg`, ...).
Usage:
    python3 scripts/export_slides.py posts/261031-01/slides.html posts/261031-02/slides.html
"""
import os
import sys
import tempfile
import subprocess
from bs4 import BeautifulSoup
from PIL import Image

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def export_slides_for_file(html_path: str) -> None:
    html_path = os.path.abspath(html_path)
    out_dir = os.path.dirname(html_path)
    with open(html_path, "r", encoding="utf-8") as f:
        raw_html = f.read()

    soup = BeautifulSoup(raw_html, "html.parser")
    styles = "\n".join(tag.decode_contents() for tag in soup.find_all("style"))
    slides = soup.find_all("div", class_="slide")

    if not slides:
        print(f"[!] No .slide elements found in {html_path}")
        return

    print(f"[*] Exporting {len(slides)} slides from {html_path} -> {out_dir}")

    with tempfile.TemporaryDirectory() as tmpdir:
        for idx, slide in enumerate(slides, start=1):
            single_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
{styles}
html, body {{
  margin: 0 !important;
  padding: 0 !important;
  width: 540px !important;
  height: 720px !important;
  overflow: hidden !important;
  background: transparent !important;
  display: block !important;
}}
.slide {{
  margin: 0 !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  width: 540px !important;
  height: 720px !important;
}}
</style>
</head>
<body>
{str(slide)}
</body>
</html>"""
            tmp_html = os.path.join(tmpdir, f"slide_{idx:02d}.html")
            tmp_png = os.path.join(tmpdir, f"slide_{idx:02d}.png")
            out_jpg = os.path.join(out_dir, f"{idx:02d}.jpg")

            with open(tmp_html, "w", encoding="utf-8") as wf:
                wf.write(single_html)

            cmd = [
                CHROME_BIN,
                "--headless=new",
                "--disable-gpu",
                "--hide-scrollbars",
                "--window-size=540,720",
                "--force-device-scale-factor=2",
                f"--screenshot={tmp_png}",
                f"file://{tmp_html}",
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            with Image.open(tmp_png) as img:
                rgb_img = img.convert("RGB")
                # Ensure exact 1080x1440 dimensions
                if rgb_img.size != (1080, 1440):
                    rgb_img = rgb_img.crop((0, 0, 1080, 1440))
                rgb_img.save(out_jpg, "JPEG", quality=95, optimize=True)
            print(f"    -> Saved {out_jpg} ({rgb_img.size[0]}x{rgb_img.size[1]})")


if __name__ == "__main__":
    for path in sys.argv[1:]:
        export_slides_for_file(path)

