"""Convert AudiQ master JSON annotations to Ultralytics YOLO detection labels.

Input: ai/annotations/master.json
Output: dataset/images/{train,val,test} and dataset/labels/{train,val,test}

The script intentionally does not infer clinical values. It only converts
verified visual bounding boxes into normalized YOLO xywh labels.
"""
from __future__ import annotations

import argparse
import json
import random
import shutil
from pathlib import Path

CLASSES = {
    "RIGHT_AC_O": 0,
    "LEFT_AC_X": 1,
    "BC": 2,
    "OTHER": 3,
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--annotations", required=True, help="Master annotation JSON")
    p.add_argument("--images-root", required=True, help="Directory containing source images")
    p.add_argument("--output", required=True, help="YOLO dataset output directory")
    p.add_argument("--val", type=float, default=0.15)
    p.add_argument("--test", type=float, default=0.15)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--copy", action="store_true", help="Copy images into output; otherwise create no image copies")
    return p.parse_args()


def split_images(images, val, test, seed):
    rng = random.Random(seed)
    items = list(images)
    rng.shuffle(items)
    n = len(items)
    n_test = round(n * test)
    n_val = round(n * val)
    return {
        "test": items[:n_test],
        "val": items[n_test:n_test + n_val],
        "train": items[n_test + n_val:],
    }


def yolo_box(box, width, height):
    x, y, w, h = box
    return x / width, y / height, w / width, h / height


def main():
    args = parse_args()
    ann_path = Path(args.annotations)
    image_root = Path(args.images_root)
    out = Path(args.output)
    data = json.loads(ann_path.read_text(encoding="utf-8"))

    records = data.get("images", [])
    if not records:
        raise SystemExit("No images found in master annotation JSON")

    splits = split_images(records, args.val, args.test, args.seed)
    for split, items in splits.items():
        (out / "images" / split).mkdir(parents=True, exist_ok=True)
        (out / "labels" / split).mkdir(parents=True, exist_ok=True)

        for item in items:
            src = image_root / item["file"]
            if not src.exists():
                raise FileNotFoundError(src)
            name = src.name
            label_path = out / "labels" / split / f"{src.stem}.txt"
            lines = []
            for symbol in item.get("symbols", []):
                cls = symbol.get("class")
                if cls not in CLASSES:
                    raise ValueError(f"Unknown class: {cls}")
                if not symbol.get("reviewer_verified", False):
                    raise ValueError(f"Unverified annotation in {item['file']}")
                x, y, w, h = yolo_box(symbol["bbox"], item["width"], item["height"])
                lines.append(f"{CLASSES[cls]} {x:.8f} {y:.8f} {w:.8f} {h:.8f}")

            label_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
            if args.copy:
                shutil.copy2(src, out / "images" / split / name)

    print(f"Created YOLO dataset at: {out}")
    print({k: len(v) for k, v in splits.items()})


if __name__ == "__main__":
    main()
