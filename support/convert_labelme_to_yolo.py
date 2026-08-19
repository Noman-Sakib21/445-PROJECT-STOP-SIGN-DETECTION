"""Convert labelme JSON annotations to YOLO .txt format.

Expects:
    data/images/*.jpg          - source images
    data/labels/*.json         - labelme annotations

Produces:
    data/labels/*.txt          - YOLO format (class_id x_center y_center w h)

Usage:
    python support/convert_labelme_to_yolo.py
"""

import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "data"
IMAGES_DIR = BASE / "images"
LABELS_DIR = BASE / "labels"

CLASS_MAP = {"stop sign": "stop_sign", "stop_sign": "stop_sign"}


def convert():
    count = 0
    for json_path in sorted(LABELS_DIR.glob("*.json")):
        data = json.loads(json_path.read_text(encoding="utf-8"))

        img_path = IMAGES_DIR / Path(data["imagePath"]).name
        if not img_path.exists():
            print(f"  WARN missing image for {json_path.name}: {img_path.name}")
            continue

        width = data.get("imageWidth")
        height = data.get("imageHeight")
        if not width or not height:
            print(f"  WARN no image size in {json_path.name}, skipping")
            continue

        lines = []
        for shape in data.get("shapes", []):
            raw_label = shape.get("label", "").strip()
            label = CLASS_MAP.get(raw_label, raw_label)
            if label != "stop_sign":
                print(f"  WARN unknown label '{raw_label}' in {json_path.name}, mapped anyway")
            pts = shape.get("points", [])
            if len(pts) != 2:
                print(f"  WARN {json_path.name}: shape has {len(pts)} points, expected 2")
                continue
            (x1, y1), (x2, y2) = pts[0], pts[1]
            x_min, x_max = min(x1, x2), max(x1, x2)
            y_min, y_max = min(y1, y2), max(y1, y2)
            if x_max <= x_min or y_max <= y_min:
                print(f"  WARN {json_path.name}: invalid box {pts}")
                continue

            xc = (x_min + x_max) / 2 / width
            yc = (y_min + y_max) / 2 / height
            bw = (x_max - x_min) / width
            bh = (y_max - y_min) / height
            lines.append(f"0 {xc:.6f} {yc:.6f} {bw:.6f} {bh:.6f}")

        txt_path = LABELS_DIR / f"{json_path.stem}.txt"
        txt_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
        count += 1

    print(f"Converted {count} label files to YOLO format in {LABELS_DIR}")


if __name__ == "__main__":
    convert()
