"""Generate synthetic audiogram charts with exact symbol ground truth.

Purpose: create a legally self-contained starter dataset when real datasets are
unavailable. Generated images are NOT patient data and are intended for model
pipeline development, not clinical validation.

Outputs:
  <out>/images/*.png
  <out>/annotations/master.json

The master JSON follows ai/ANNOTATION_SCHEMA.md. A later conversion step can
turn the verified boxes into YOLO labels.
"""
from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FREQS = [125, 250, 500, 1000, 2000, 4000, 8000]
CLASS_INFO = {"RIGHT_AC_O": ("right", "air", "O"), "LEFT_AC_X": ("left", "air", "X"), "BC": (None, "bone", "<")}


def font(size: int):
    for name in ("DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def make_curve(rng, base: int):
    vals = []
    v = base
    for i in range(len(FREQS)):
        if i:
            v += rng.choice([-10, -5, 0, 0, 5, 5, 10])
        vals.append(max(-10, min(120, round(v / 5) * 5)))
    return vals


def draw_chart(path: Path, idx: int, rng: random.Random):
    W, H = 1000, 760
    left, top, right, bottom = 120, 100, 900, 680
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    title_font = font(28)
    label_font = font(18)
    symbol_font = font(26)
    d.text((W // 2, 35), "AUDIQ SYNTHETIC AUDIOGRAM", anchor="mm", font=title_font, fill="black")

    # Grid and axes. Slight layout variants create visual diversity.
    y_step = 5 if idx % 3 else 10
    dbs = list(range(-10, 121, y_step))
    x_positions = [left + (right-left) * i / (len(FREQS)-1) for i in range(len(FREQS))]
    def y(db): return top + (db + 10) / 130 * (bottom-top)
    for db in dbs:
        yy = y(db)
        d.line((left, yy, right, yy), fill=(205,205,205), width=1)
        if db % 10 == 0:
            d.text((left-12, yy), str(db), anchor="rm", font=label_font, fill="black")
    for x, f in zip(x_positions, FREQS):
        d.line((x, top, x, bottom), fill=(205,205,205), width=1)
        d.text((x, top-18), str(f), anchor="ms", font=label_font, fill="black")
    d.line((left, top, left, bottom), fill="black", width=2)
    d.line((left, bottom, right, bottom), fill="black", width=2)
    d.text((35, (top+bottom)//2), "Hearing level (dB HL)", anchor="mm", font=label_font, fill="black")

    right_vals = make_curve(rng, rng.choice([10, 20, 35, 55, 75]))
    left_vals = make_curve(rng, rng.choice([10, 25, 40, 60, 80]))
    # Sometimes keep ears close; sometimes deliberately asymmetric.
    if idx % 4 == 0:
        left_vals = [min(120, v+20) for v in right_vals]
    records = []
    points = {}
    for cls, vals in (("RIGHT_AC_O", right_vals), ("LEFT_AC_X", left_vals)):
        pts = [(x_positions[i], y(vals[i])) for i in range(len(FREQS))]
        points[cls] = pts
        d.line([p for pt in pts for p in (pt,)], fill=(210,40,60) if cls.startswith("RIGHT") else (35,85,180), width=2)
        for (x, yy), f, db in zip(pts, FREQS, vals):
            sym = "O" if cls == "RIGHT_AC_O" else "X"
            fill = (210,40,60) if sym == "O" else (35,85,180)
            d.text((x, yy), sym, anchor="mm", font=symbol_font, fill=fill, stroke_width=1, stroke_fill=fill)
            records.append({"class": cls, "bbox": [round(x), round(yy), 30, 30], "ear": "right" if cls.startswith("RIGHT") else "left", "conduction": "air", "masked": False, "frequency_hz": f, "threshold_db_hl": db, "annotation_confidence": 1.0, "reviewer_verified": True})

    # Optional BC symbols, with shared class because initial detector does not encode ear.
    if idx % 2 == 0:
        for i in [1, 2, 4]:
            db = max(-10, left_vals[i] - 15)
            x, yy = x_positions[i], y(db)
            d.text((x, yy), "<", anchor="mm", font=symbol_font, fill=(20,150,80))
            records.append({"class": "BC", "bbox": [round(x), round(yy), 30, 30], "ear": None, "conduction": "bone", "masked": bool(idx % 4 == 0), "frequency_hz": FREQS[i], "threshold_db_hl": db, "annotation_confidence": 1.0, "reviewer_verified": True})

    im.save(path)
    return {"image_id": f"synthetic_{idx:04d}", "file": path.name, "width": W, "height": H, "review_status": "verified", "symbols": records}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="synthetic_audiograms")
    ap.add_argument("--count", type=int, default=200)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    out = Path(args.out)
    img_dir = out / "images"
    ann_dir = out / "annotations"
    img_dir.mkdir(parents=True, exist_ok=True)
    ann_dir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(args.seed)
    records = [draw_chart(img_dir / f"synthetic_{i:04d}.png", i, rng) for i in range(args.count)]
    (ann_dir / "master.json").write_text(json.dumps({"schema_version":"0.1","created_by":"AudiQ synthetic generator","purpose":"synthetic audiogram visual-symbol dataset","images":records}, indent=2), encoding="utf-8")
    print(f"Generated {len(records)} synthetic audiograms in {out}")


if __name__ == "__main__":
    main()
