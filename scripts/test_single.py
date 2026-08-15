"""Manually test the model on one image and show the result on screen.

Usage:
    python scripts/test_single.py <image_path>

The annotated image is saved to runs/detections/ and shown in a window.
"""

import sys
from pathlib import Path

import cv2
from ultralytics import YOLO

BASE = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE / "models" / "stop_sign_detector.pt"
OUT_DIR = BASE / "runs" / "detections"
OUT_DIR.mkdir(parents=True, exist_ok=True)

STOP_CLASS_IDS = {0}
CONF = 0.4

if len(sys.argv) < 2:
    print("Usage: python scripts/test_single.py <image_path>")
    sys.exit(1)

img_path = Path(sys.argv[1])
if not img_path.exists():
    print(f"File not found: {img_path}")
    sys.exit(1)

model = YOLO(MODEL_PATH)
img = cv2.imread(str(img_path))
if img is None:
    print(f"Could not read image: {img_path}")
    sys.exit(1)

results = model(img, imgsz=640)[0]
detections = 0
for box in results.boxes:
    if int(box.cls[0]) not in STOP_CLASS_IDS:
        continue
    x1, y1, x2, y2 = map(int, box.xyxy[0])
    conf = float(box.conf[0])
    if conf >= CONF:
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
        cv2.putText(img, f"Stop {conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        detections += 1

out_path = OUT_DIR / f"{img_path.stem}_detected{img_path.suffix.lower()}"
cv2.imwrite(str(out_path), img)
print(f"Detected {detections} stop sign(s).")
print(f"Saved to: {out_path}")

cv2.imshow("Detection Result - press any key to close", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
