"""Stop Sign Detection in Street Images — Main entry point.

CSE445 Semester Project (Group 8)

Run:
    python main.py                    # detect on the validation dataset
    python main.py path/to/photo.jpg  # detect on a single image
    python main.py images/...         # detect on multiple images or a folder

Output images (with red bounding boxes and confidence labels) are written to
runs/detections/ and the console shows the number of stop signs found per image.
"""

import sys
from pathlib import Path

from ultralytics import YOLO

BASE = Path(__file__).resolve().parent

MODEL_CANDIDATES = [
    BASE / "models" / "stop_sign_detector.pt",
    BASE / "support" / "models" / "stop_sign_detector.pt",
]
MODEL_PATH = next((m for m in MODEL_CANDIDATES if m.exists()), MODEL_CANDIDATES[0])

OUTPUT_DIR = BASE / "runs" / "detections"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CONF = 0.4
IMGSZ = 640
STOP_CLASS_IDS = {0}


def collect_images(args):
    """Resolve CLI arguments into a list of image files."""
    if not args:
        default_dir = BASE / "data" / "val" / "images"
        if default_dir.exists():
            print(f"No input given — running on validation set: {default_dir}")
            return sorted(default_dir.glob("*.jpg"))
        print("No input given and no validation set found. Usage: python main.py <image...>")
        sys.exit(1)

    images = []
    for arg in args:
        p = Path(arg)
        if p.is_dir():
            images.extend(sorted(x for x in p.glob("*") if x.suffix.lower() in (".jpg", ".jpeg", ".png")))
        elif p.is_file():
            images.append(p)
        else:
            print(f"Warning: {p} not found, skipped.")
    return images


def main():
    model = YOLO(str(MODEL_PATH))
    images = collect_images(sys.argv[1:])

    if not images:
        print("No images to process.")
        sys.exit(1)

    print(f"Model: {MODEL_PATH}")
    print(f"Processing {len(images)} image(s)...")
    total_signs = 0

    for i, img in enumerate(images, 1):
        result = model(str(img), conf=CONF, imgsz=IMGSZ)[0]
        boxes = [b for b in result.boxes if int(b.cls[0]) in STOP_CLASS_IDS]

        annotated = result.plot()  # draws boxes + labels
        out_path = OUTPUT_DIR / f"{img.stem}_detected.jpg"
        import cv2
        cv2.imwrite(str(out_path), annotated)

        total_signs += len(boxes)
        print(f"  {img.name}: {len(boxes)} stop sign(s) -> {out_path.name}")

    print(f"\nDone. {total_signs} stop sign(s) detected in total.")
    print(f"Results saved in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()