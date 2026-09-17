# AudiQ AI v0.1 — Kaggle/Colab starter
# Paste into a notebook cell or run as a Python script after attaching a YOLO dataset.

from ultralytics import YOLO

# 1) Install once in Kaggle/Colab:
# !pip install -q -r /kaggle/input/audiq-repo/ai/requirements.txt

# 2) Set this to the dataset YAML path in your Kaggle dataset.
DATA = '/kaggle/input/audiq-dataset/dataset.yaml'

# 3) Start from a pretrained detector; fine-tune on audiogram symbols.
model = YOLO('yolov8n.pt')

results = model.train(
    data=DATA,
    epochs=50,
    imgsz=960,
    batch=-1,
    patience=15,
    pretrained=True,
    project='/kaggle/working/audiq_runs',
    name='symbol_v0_1',
)

# 4) Validation metrics.
metrics = model.val(data=DATA, imgsz=960)
print(metrics)

# 5) Export a deployment-friendly model after validation.
model.export(format='onnx')
