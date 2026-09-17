# AudiQ AI Lab v0.1

This folder contains the reproducible computer-vision training pipeline for AudiQ.

## Current goal

The first model is **audiogram visual-symbol detection**, not autonomous clinical interpretation.

Target classes:

1. `RIGHT_AC_O`
2. `LEFT_AC_X`
3. `BC`
4. `OTHER`

## What is already built

- `ANNOTATION_STUDIO.html` — browser annotation tool for O/X/BC/other marks.
- `ANNOTATION_SCHEMA.md` — master JSON annotation contract.
- `generate_synthetic_dataset.py` — creates legally self-contained synthetic audiograms with exact ground truth.
- `convert_annotations.py` — converts verified master JSON to YOLO labels.
- `prepare_dataset.py` / `validate_dataset.py` — dataset checks.
- `AudiQ_AI_Training_v0_1.ipynb` — Kaggle/Colab training starter.
- `train.py` / `predict.py` — training and inference entry points.

## First experiment: synthetic baseline

When a public/permissioned real dataset is unavailable, start with synthetic data to verify the entire pipeline:

```bash
python ai/generate_synthetic_dataset.py --out synthetic_audiograms --count 200
python ai/convert_annotations.py --annotations synthetic_audiograms/annotations/master.json --images-root synthetic_audiograms/images --output dataset --copy
python ai/prepare_dataset.py --root dataset
```

Then train in Kaggle/Colab using `ai/AudiQ_AI_Training_v0_1.ipynb`.

Synthetic training is a **pipeline/engineering baseline only**. It must not be presented as clinical validation because synthetic charts do not represent the full variation of real audiograms, scanning, printing, handwriting, symbols, or clinical records.

## Test policy

The five seed audiograms supplied for the first AudiQ experiment are held out from training and validation. They are for final pipeline testing after a model has been trained on independent data.

## Data policy

Only use de-identified data for development. Do not commit patient images, clinical identifiers, restricted research datasets, or third-party weights without permission to this public repository.

## Pipeline

`image -> chart/symbol detection -> coordinates -> frequency/dB mapping -> confidence -> human verification -> clinical calculations`

Clinical calculations remain outside the model and must use verified thresholds.

## Safety boundary

AudiQ AI is an experimental research/engineering component. It does not independently establish hearing-loss diagnosis, masking requirements, SRT, or clinical management. Model outputs require human verification before clinical calculations or reporting.
