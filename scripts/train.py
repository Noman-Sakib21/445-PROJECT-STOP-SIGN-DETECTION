"""Train the YOLOv8 stop sign detector from scratch on your own dataset.

Trains from random weights (yolov8n.yaml architecture) -- NO COCO pretrained
weights are used. Every stop sign pattern is learned from your 50 images.

Note: 50 images is a small dataset, so expect lower accuracy than the COCO
pretrained model. More epochs help.

Usage:
    python scripts/train.py
"""

from pathlib import Path

from ultralytics import YOLO

BASE = Path(__file__).resolve().parent.parent

model = YOLO("yolov8n.yaml")

results = model.train(
    data=str(BASE / "dataset.yaml"),
    epochs=300,
    imgsz=640,
    batch=8,
    patience=40,
    device="cpu",
    workers=0,
    name="stop_sign_detector_from_scratch",
    project=str(BASE / "runs"),
    plots=True,
)

print("Training complete!")
print("Best model:", BASE / "runs" / "stop_sign_detector_from_scratch" / "weights" / "best.pt")
