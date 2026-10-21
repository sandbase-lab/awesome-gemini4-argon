#!/usr/bin/env python3
"""Build assets/banner.png (1280x640): the README header and the GitHub social preview.

A 4x2 wall of the featured posters (from SandBase Lab) under a dark band with the title.
Run locally after the featured list changes; needs Pillow. Fonts: macOS system fonts,
falls back to Pillow's default.
"""
import io
import json
import pathlib
import urllib.request

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[1]
W, H = 1280, 640
videos = json.loads((ROOT / 'data/videos.json').read_text())
# Finished Argon pieces only: no comparisons (they show other models' names) and no talking heads.
SKIP = ('vs', 'versus', 'comparison', 'compar', 'opus', 'gpt', 'claude', 'benchmark', 'test')
CREATIVE = ('3d-scene', 'game', 'motion-graphics', 'particles')
ok = lambda v: v['poster'] and v['category'] in CREATIVE and not any(w in v['title'].lower() for w in SKIP)
# Hand-checked fallbacks if the automatic pick ever needs overriding: list ids here.
PINNED = [i for i in (ROOT / 'assets' / 'banner-ids.txt').read_text().split() if i] if (ROOT / 'assets' / 'banner-ids.txt').exists() else []
by_id = {v['id']: v for v in videos}
picks = [by_id[i] for i in PINNED if i in by_id and by_id[i]['poster']]
picks += sorted((v for v in videos if ok(v) and v['featured'] is not None and v not in picks), key=lambda v: v['featured'])
picks += [v for v in videos if ok(v) and v not in picks]
# Few posts in those categories: fill with any other finished poster rather than leave cells dark.
picks += [v for v in videos if v['poster'] and not any(w in v['title'].lower() for w in SKIP) and v not in picks]
picks = picks[:8]


def font(size, bold=True):
    for path, index in (('/System/Library/Fonts/HelveticaNeue.ttc', 1 if bold else 0), ('/System/Library/Fonts/Helvetica.ttc', 1 if bold else 0)):
        try:
            return ImageFont.truetype(path, size, index=index)
        except OSError:
            continue
    return ImageFont.load_default()


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'awesome-gemini4-argon-banner/1.0'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return Image.open(io.BytesIO(r.read())).convert('RGB')


def cover(img, w, h):
    scale = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    left, top = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((left, top, left + w, top + h))


canvas = Image.new('RGB', (W, H), (10, 10, 14))
cols, rows, gap = 4, 2, 6
cw, ch = (W - gap * (cols + 1)) // cols, (H - gap * (rows + 1)) // rows
for i, v in enumerate(picks):
    x, y = gap + (i % cols) * (cw + gap), gap + (i // cols) * (ch + gap)
    canvas.paste(cover(fetch(v['poster']), cw, ch), (x, y))

# Dark band for legible text, blurred behind.
band_top, band_h = 200, 240
band = canvas.crop((0, band_top, W, band_top + band_h)).filter(ImageFilter.GaussianBlur(12))
shade = Image.new('RGB', band.size, (8, 8, 12))
canvas.paste(Image.blend(band, shade, 0.78), (0, band_top))

d = ImageDraw.Draw(canvas)
title, sub = 'Awesome Gemini 4 Argon', 'Videos · prompts · tutorial · model comparison'
tf, sf = font(76), font(32, bold=False)
tw = d.textlength(title, font=tf)
d.text(((W - tw) / 2, band_top + 46), title, font=tf, fill=(255, 255, 255))
sw = d.textlength(sub, font=sf)
d.text(((W - sw) / 2, band_top + 146), sub, font=sf, fill=(200, 205, 220))

out = ROOT / 'assets' / 'banner.png'
out.parent.mkdir(exist_ok=True)
canvas.save(out, optimize=True)
print(f'Saved {out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB) from {len(picks)} posters.')
