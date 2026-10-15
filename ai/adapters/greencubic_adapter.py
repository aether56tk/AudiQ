"""Normalize audiogram digitization output into AudiQ's point schema.

This adapter is intentionally tolerant: third-party projects may serialize
detections as JSON lists, nested records, or slightly different field names.
It does not infer missing ear/frequency/threshold values.

Usage:
  python ai/adapters/greencubic_adapter.py input.json --output audiq_predictions.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

EAR_KEYS = ("ear", "side", "ear_side")
CONDUCTION_KEYS = ("conduction", "type", "mode")
FREQ_KEYS = ("frequency_hz", "frequency", "freq", "hz")
THRESHOLD_KEYS = ("threshold_db_hl", "threshold", "db_hl", "db")
CONF_KEYS = ("confidence", "score", "probability")
MASKED_KEYS = ("masked", "masking")


def first(record, keys):
    for key in keys:
        if key in record and record[key] not in (None, ""):
            return record[key]
    return None


def flatten(obj):
    if isinstance(obj, list):
        return [x for x in obj if isinstance(x, dict)]
    if not isinstance(obj, dict):
        return []
    for key in ("predictions", "detections", "points", "symbols", "results", "data"):
        value = obj.get(key)
        if isinstance(value, list):
            return [x for x in value if isinstance(x, dict)]
    return [obj]


def normalize(record, source_index):
    ear = first(record, EAR_KEYS)
    conduction = first(record, CONDUCTION_KEYS)
    freq = first(record, FREQ_KEYS)
    threshold = first(record, THRESHOLD_KEYS)
    confidence = first(record, CONF_KEYS)
    masked = first(record, MASKED_KEYS)

    if isinstance(ear, str):
        ear = ear.strip().lower()
        if ear in {"r", "rt"}: ear = "right"
        if ear in {"l", "lt"}: ear = "left"

    if isinstance(conduction, str):
        conduction = conduction.strip().lower()
        if conduction in {"ac", "air-conduction", "air conduction"}: conduction = "air"
        if conduction in {"bc", "bone-conduction", "bone conduction"}: conduction = "bone"

    try:
        freq = int(round(float(freq))) if freq is not None else None
    except (TypeError, ValueError):
        freq = None
    try:
        threshold = float(threshold) if threshold is not None else None
    except (TypeError, ValueError):
        threshold = None
    try:
        confidence = float(confidence) if confidence is not None else None
    except (TypeError, ValueError):
        confidence = None

    return {
        "source_index": source_index,
        "ear": ear,
        "conduction": conduction,
        "masked": bool(masked) if masked is not None else None,
        "frequency_hz": freq,
        "threshold_db_hl": threshold,
        "confidence": confidence,
        "needs_review": any(v is None for v in (ear, conduction, freq, threshold)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("--output", type=Path, default=Path("audiq_predictions.json"))
    args = ap.parse_args()

    raw = json.loads(args.input.read_text(encoding="utf-8"))
    records = flatten(raw)
    normalized = [normalize(r, i) for i, r in enumerate(records)]

    payload = {
        "schema_version": "0.1",
        "source": str(args.input),
        "predictions": normalized,
        "verification_required": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Normalized {len(normalized)} records -> {args.output}")


if __name__ == "__main__":
    main()
