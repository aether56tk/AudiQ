# AudiQ AI — Dataset Setup

## Purpose

Prepare a permitted audiogram dataset for the first AudiQ computer-vision experiment.

## Do not upload

- Patient names, IDs, phone numbers, addresses, dates of birth, or other direct identifiers.
- Clinical photographs containing identifying information.
- Restricted third-party datasets or pretrained weights unless their terms explicitly permit the intended use.

## YOLO layout

```text
dataset/
├── dataset.yaml
├── images/
│   ├── train/
│   ├── val/
│   └── test/
└── labels/
    ├── train/
    ├── val/
    └── test/
```

## Initial classes

| ID | Class |
|---:|---|
| 0 | RIGHT_AC_O |
| 1 | LEFT_AC_X |
| 2 | BC |
| 3 | OTHER |

Labels use standard YOLO normalized bounding boxes:

```text
class_id x_center y_center width height
```

## Recommended workflow

1. Obtain the permitted dataset and keep the original archive unchanged.
2. Convert/copy only the permitted images and annotations into the YOLO structure.
3. Run `python ai/prepare_dataset.py --root dataset`.
4. Inspect class counts and missing-label warnings.
5. Train in Kaggle/Colab with `ai/AudiQ_AI_Training_v0_1.ipynb`.
6. Keep the test set untouched until final evaluation.
7. Record model metrics and threshold/frequency errors.

## Important

The initial model is a symbol detector. It is not a validated audiogram interpreter. Any threshold candidates produced by the model require human verification before clinical calculations.
