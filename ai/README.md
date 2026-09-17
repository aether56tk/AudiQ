# AudiQ AI Lab v0.1

This folder contains the reproducible computer-vision training pipeline for AudiQ.

## Tonight's baseline

The first task is **audiogram symbol detection**, not autonomous clinical interpretation.

Target classes for the initial dataset:

1. `RIGHT_AC_O`
2. `LEFT_AC_X`
3. `BC`
4. `OTHER`

The pipeline is designed to work with YOLO-compatible datasets and can be run locally or in Kaggle/Colab.

## Research baselines to inspect

- GreenCUBIC AudiogramDigitization: https://github.com/GreenCUBIC/AudiogramDigitization
- MAIN2021: https://github.com/jacklishufan/MAIN2021
- AutoAudiogram: https://github.com/biodatlab/autoaudiogram
- SyntHH: https://github.com/evidENT-AI/SyntHH

These projects are references/baselines. Their code and datasets have different licenses and access conditions; do not copy restricted datasets into this repository without permission.

## Data policy

Only use de-identified data for development. Do not commit patient images, clinical identifiers, or restricted research datasets to this public repository.

## Pipeline

`images -> annotation -> YOLO dataset -> training -> validation -> test -> threshold extraction -> human verification`

Clinical calculations remain outside the model and must use verified thresholds.
