# AudiQ AI v0.1 Smoke Test

## 1. Generate
python ai/generate_synthetic_dataset.py --out synthetic_audiograms --count 200

Expected: 200 PNG audiograms and annotations/master.json with exact synthetic ground truth.

## 2. Convert
python ai/convert_annotations.py --annotations synthetic_audiograms/annotations/master.json --images-root synthetic_audiograms/images --output dataset --copy

Expected: train/val/test images and matching YOLO labels.

## 3. Validate
python ai/prepare_dataset.py --root dataset

## 4. Train
python ai/train.py --data dataset/dataset.yaml --model yolov8n.pt --epochs 50 --imgsz 960

## 5. Evaluate
Record precision, recall, mAP, threshold MAE, ±5 dB and ±10 dB accuracy, frequency assignment accuracy, and manual correction rate.

## Test-set rule
Keep the test split untouched during training and tuning. Human verification is required before clinical calculations.