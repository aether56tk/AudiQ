"""AudiQ AI baseline trainer.

Usage:
  python train.py --data dataset.yaml --model yolov8n.pt --epochs 50

This trains only the visual symbol detector. Clinical interpretation is intentionally
outside the model and requires verified thresholds.
"""
import argparse
from pathlib import Path
from ultralytics import YOLO


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--data', default='dataset.yaml')
    p.add_argument('--model', default='yolov8n.pt')
    p.add_argument('--epochs', type=int, default=50)
    p.add_argument('--imgsz', type=int, default=960)
    p.add_argument('--batch', type=int, default=-1)
    p.add_argument('--device', default=None, help='0 for GPU, cpu for CPU')
    p.add_argument('--project', default='runs/audiq')
    p.add_argument('--name', default='symbol-v0.1')
    args = p.parse_args()

    model = YOLO(args.model)
    results = model.train(
        data=args.data,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device,
        project=args.project,
        name=args.name,
        patience=15,
        pretrained=True,
        verbose=True,
    )
    print('Training complete.')
    print(f'Results: {Path(results.save_dir)}')


if __name__ == '__main__':
    main()
