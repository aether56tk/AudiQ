"""Validate an AudiQ YOLO detection dataset before training."""
from __future__ import annotations

import argparse
from pathlib import Path

CLASS_NAMES = {0: "RIGHT_AC_O", 1: "LEFT_AC_X", 2: "BC", 3: "OTHER"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("dataset", type=Path)
    args = p.parse_args()
    root = args.dataset
    errors = []
    total_images = 0
    total_boxes = 0

    for split in ("train", "val", "test"):
        image_dir = root / "images" / split
        label_dir = root / "labels" / split
        if not image_dir.exists():
            errors.append(f"Missing {image_dir}")
            continue
        if not label_dir.exists():
            errors.append(f"Missing {label_dir}")
            continue

        images = [p for p in image_dir.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}]
        total_images += len(images)
        for img in images:
            label = label_dir / f"{img.stem}.txt"
            if not label.exists():
                errors.append(f"Missing label: {label}")
                continue
            for line_no, line in enumerate(label.read_text(encoding="utf-8").splitlines(), 1):
                parts = line.split()
                if len(parts) != 5:
                    errors.append(f"{label}:{line_no}: expected 5 fields")
                    continue
                try:
                    cls = int(parts[0])
                    vals = [float(x) for x in parts[1:]]
                except ValueError:
                    errors.append(f"{label}:{line_no}: non-numeric value")
                    continue
                if cls not in CLASS_NAMES:
                    errors.append(f"{label}:{line_no}: unknown class {cls}")
                if any(v < 0 or v > 1 for v in vals):
                    errors.append(f"{label}:{line_no}: coordinates must be normalized 0..1")
                total_boxes += 1

    print(f"Images: {total_images}")
    print(f"Boxes:  {total_boxes}")
    if errors:
        print(f"ERRORS: {len(errors)}")
        for e in errors[:100]:
            print(" -", e)
        raise SystemExit(1)
    print("Dataset validation passed.")


if __name__ == "__main__":
    main()
