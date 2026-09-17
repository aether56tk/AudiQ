"""AudiQ AI v0.1 - validate and prepare a YOLO dataset.

Expected layout:
  dataset/
    images/{train,val,test}/
    labels/{train,val,test}/
    dataset.yaml

YOLO label format: class_id x_center y_center width height (normalized 0..1).
This script does not download or copy third-party datasets. It validates a local
working copy and reports problems before training.
"""
from pathlib import Path
import argparse
import yaml

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
CLASS_NAMES = ["RIGHT_AC_O", "LEFT_AC_X", "BC", "OTHER"]


def read_labels(path: Path):
    if not path.exists():
        return []
    rows = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) != 5:
            raise ValueError(f"{path}:{line_no}: expected 5 fields, got {len(parts)}")
        cls = int(float(parts[0]))
        vals = [float(x) for x in parts[1:]]
        if not 0 <= cls < len(CLASS_NAMES):
            raise ValueError(f"{path}:{line_no}: class {cls} outside 0..{len(CLASS_NAMES)-1}")
        if any(v < 0 or v > 1 for v in vals):
            raise ValueError(f"{path}:{line_no}: coordinates must be normalized 0..1")
        rows.append(cls)
    return rows


def validate_split(root: Path, split: str):
    image_dir = root / "images" / split
    label_dir = root / "labels" / split
    images = sorted(p for p in image_dir.glob("*") if p.suffix.lower() in IMAGE_EXTS)
    missing = []
    counts = [0] * len(CLASS_NAMES)
    objects = 0
    for image in images:
        label = label_dir / f"{image.stem}.txt"
        if not label.exists():
            missing.append(image.name)
            continue
        for cls in read_labels(label):
            counts[cls] += 1
            objects += 1
    return len(images), objects, counts, missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="dataset", help="YOLO dataset root")
    args = ap.parse_args()
    root = Path(args.root)
    yaml_path = root / "dataset.yaml"
    if not yaml_path.exists():
        raise SystemExit(f"Missing {yaml_path}")
    config = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    print("AudiQ dataset validator")
    print("Classes:", CLASS_NAMES)
    print("YAML names:", config.get("names"))
    total = 0
    for split in ("train", "val", "test"):
        n_images, n_objects, counts, missing = validate_split(root, split)
        total += n_images
        print(f"\n[{split}] images={n_images}, objects={n_objects}")
        print(dict(zip(CLASS_NAMES, counts)))
        if missing:
            print(f"WARNING: {len(missing)} images have no label file")
            print("  ", ", ".join(missing[:10]))
    if total == 0:
        raise SystemExit("No images found. Add the permitted dataset under dataset/images first.")
    print("\nValidation complete. Review class balance and warnings before training.")


if __name__ == "__main__":
    main()
