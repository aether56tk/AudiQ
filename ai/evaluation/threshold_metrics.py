"""Evaluate threshold predictions against verified ground truth.

Matching key: ear + conduction + frequency + masked.
Primary metric: absolute threshold error in dB HL.

Example:
  python ai/evaluation/threshold_metrics.py gt.json pred.json
"""
from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path


def load_points(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    points = data.get("predictions", data.get("points", data.get("symbols", data)))
    if not isinstance(points, list):
        raise ValueError(f"{path}: expected a list or a JSON object containing predictions/points/symbols")
    return points


def key(p):
    return (
        str(p.get("ear", "")).lower(),
        str(p.get("conduction", "")).lower(),
        int(p["frequency_hz"]),
        bool(p.get("masked", False)),
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ground_truth", type=Path)
    ap.add_argument("predictions", type=Path)
    args = ap.parse_args()

    gt = {key(p): p for p in load_points(args.ground_truth)}
    pred = {key(p): p for p in load_points(args.predictions)}

    errors = []
    within_5 = within_10 = 0
    missing = extra = 0

    for k, g in gt.items():
        if k not in pred:
            missing += 1
            continue
        try:
            err = abs(float(pred[k]["threshold_db_hl"]) - float(g["threshold_db_hl"]))
        except (KeyError, TypeError, ValueError):
            missing += 1
            continue
        errors.append(err)
        within_5 += err <= 5
        within_10 += err <= 10

    extra = len(set(pred) - set(gt))

    print(f"Ground-truth points: {len(gt)}")
    print(f"Predicted points:     {len(pred)}")
    print(f"Matched points:       {len(errors)}")
    print(f"Missing points:       {missing}")
    print(f"Extra points:         {extra}")

    if not errors:
        print("No matched points to score.")
        return

    print(f"MAE (dB HL):          {statistics.mean(errors):.2f}")
    print(f"Median abs error:     {statistics.median(errors):.2f}")
    print(f"Within ±5 dB:         {within_5/len(errors):.3f}")
    print(f"Within ±10 dB:        {within_10/len(errors):.3f}")


if __name__ == "__main__":
    main()
