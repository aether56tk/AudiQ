# AudiQ AI Annotation Schema v0.1

This schema separates **visual detection** from **clinical interpretation**.

## 1. Visual classes

| Class | Meaning |
|---|---|
| `RIGHT_AC_O` | Right-ear air-conduction O symbol |
| `LEFT_AC_X` | Left-ear air-conduction X symbol |
| `BC` | Bone-conduction symbol when the exact ear is not encoded by the detector |
| `OTHER` | Other audiogram mark that should not be used directly for threshold calculation |

## 2. Master annotation format

One JSON file can contain one or more images:

```json
{
  "schema_version": "0.1",
  "images": [
    {
      "image_id": "example_001",
      "file": "example_001.png",
      "width": 1200,
      "height": 900,
      "review_status": "verified",
      "symbols": [
        {
          "class": "RIGHT_AC_O",
          "bbox": [590, 340, 18, 18],
          "ear": "right",
          "conduction": "air",
          "masked": false,
          "frequency_hz": 1000,
          "threshold_db_hl": 30,
          "annotation_confidence": 1.0,
          "reviewer_verified": true
        }
      ]
    }
  ]
}
```

`bbox` is `[x_center_px, y_center_px, width_px, height_px]`.

## 3. Rules

- Annotate the **symbol itself**, not the whole audiogram line.
- Use a small box around the center of O/X/BC marks.
- Do not use the connecting line as the object box.
- `frequency_hz` and `threshold_db_hl` are ground-truth metadata and are not inferred from the detector class.
- Keep `masked` explicit when known.
- If a mark cannot be confidently identified, use `OTHER` rather than guessing.
- If a symbol overlaps another symbol, annotate each visible symbol separately when its center can be established.
- Do not put patient identifiers in annotation metadata.

## 4. Train/validation/test policy

The five seed audiograms supplied for the first AudiQ experiment are treated as **held-out test images**. They must not be used for training or validation.

For the first trainable dataset, use independent public/licensed images or newly created synthetic audiograms. Keep dataset licensing information in `DATA_SOURCES.md`.

## 5. Clinical safety boundary

The model detects visual marks. It does not independently establish hearing-loss diagnosis, masking requirements, SRT, or clinical management. Thresholds extracted by the model must be verified by a clinician before AudiQ performs clinical calculations.
