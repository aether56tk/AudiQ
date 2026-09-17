"""AudiQ inference helper.

Usage:
  python predict.py --model runs/audiq/symbol-v0.1/weights/best.pt --source path/to/image.jpg

Outputs YOLO detections plus a CSV for later threshold-mapping work.
"""
import argparse
from pathlib import Path
import csv
from ultralytics import YOLO


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--model', required=True)
    p.add_argument('--source', required=True)
    p.add_argument('--conf', type=float, default=0.25)
    p.add_argument('--output', default='runs/predict/audiq_detections.csv')
    args = p.parse_args()

    model = YOLO(args.model)
    rows = []
    for result in model.predict(source=args.source, conf=args.conf, save=True, verbose=False):
        names = result.names
        if result.boxes is None:
            continue
        for b in result.boxes:
            cls = int(b.cls.item())
            conf = float(b.conf.item())
            x1, y1, x2, y2 = [float(v) for v in b.xyxy[0].tolist()]
            rows.append([str(result.path), cls, names[cls], conf, x1, y1, x2, y2])

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['image','class_id','class_name','confidence','x1','y1','x2','y2'])
        w.writerows(rows)
    print(f'Saved {len(rows)} detections to {out}')


if __name__ == '__main__':
    main()
