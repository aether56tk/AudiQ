"""One-command synthetic baseline for AudiQ AI.

Generates a synthetic dataset, converts verified annotations to YOLO, validates
the result, and prints the exact command for GPU training.
"""
from __future__ import annotations
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def run(*args):
    print("\n$", " ".join(map(str, args)))
    subprocess.run([sys.executable, *map(str, args)], check=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=200)
    ap.add_argument("--out", default="synthetic_audiograms")
    ap.add_argument("--dataset", default="dataset")
    args = ap.parse_args()
    out = Path(args.out)
    dataset = Path(args.dataset)
    run(ROOT / "generate_synthetic_dataset.py", "--out", out, "--count", args.count)
    run(ROOT / "convert_annotations.py", "--annotations", out / "annotations" / "master.json", "--images-root", out / "images", "--output", dataset, "--copy")
    run(ROOT / "prepare_dataset.py", "--root", dataset)
    print("\nSynthetic baseline is ready.")
    print(f"Train in Kaggle/Colab with: python ai/train.py --data {dataset / "dataset.yaml"} --model yolov8n.pt --epochs 50 --imgsz 960")
    print("Synthetic results are engineering/pipeline results, not clinical validation.")

if __name__ == "__main__":
    main()