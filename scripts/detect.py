"""Run stop sign detection on new images.

Usage:
    python scripts/detect.py [image_path...]

Examples:
    python scripts/detect.py test1.jpg
    python scripts/detect.py img1.jpg img2.jpg test_folder/
    python scripts/detect.py                          # runs on dataset/val/images
"""

import sys
from pathlib import Path

import cv2
from ultralytics import YOLO

BASE = Path(__file__).resolve().parent.parent
_MODELS = [
    BASE / "models" / "stop_sign_detector.pt",
    BASE / "runs" / "stop_sign_detector" / "weights" / "best.pt",
]
MODEL_PATH = next((m for m in _MODELS if m.exists()), _MODELS[0])

STOP_CLASS_IDS = {0}
CONF = 0.4

OUTPUT_DIR = BASE / "runs" / "detections"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def collect_targets(args):
    if not args:
        return sorted((BASE / "dataset" / "val" / "images").iterdir())
    targets = []
    for arg in args:
        p = Path(arg)
        if p.is_dir():
            targets.extend(p.iterdir())
        else:
            targets.append(p)
    return [t for t in targets if t.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp"}]


def main():
    if not MODEL_PATH.exists():
        print("Model not found. Train first:  python scripts/train.py")
        print("Expected:", MODEL_PATH)
        sys.exit(1)

    model = YOLO(MODEL_PATH)
    targets = collect_targets(sys.argv[1:])

    if not targets:
        print("No images found to process.")
        sys.exit(1)

    print(f"Processing {len(targets)} image(s)...")
    for path in targets:
        img = cv2.imread(str(path))
        if img is None:
            print(f"  SKIP (could not read): {path}")
            continue

        results = model(img, imgsz=640)[0]
        detections = 0
        for box in results.boxes:
            cls = int(box.cls[0])
            if cls not in STOP_CLASS_IDS:
                continue
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            if conf >= CONF:
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
                cv2.putText(
                    img,
                    f"Stop {conf:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                )
                detections += 1

        out_path = OUTPUT_DIR / f"{path.stem}_detected{path.suffix.lower()}"
        cv2.imwrite(str(out_path), img)
        print(f"  {path.name}: {detections} stop sign(s) -> {out_path.name}")

    print("\nDone. Results saved to:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
