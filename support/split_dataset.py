"""Split the annotated dataset into train and val.

Val images are chosen by explicit number: stop_001..stop_008 and stop_064, stop_065.
Everything else goes to train.

Usage:
    python support/split_dataset.py
"""

import re
import shutil
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "data"
IMAGES = BASE / "images"
LABELS = BASE / "labels"

TRAIN_IMAGES = BASE / "train" / "images"
TRAIN_LABELS = BASE / "train" / "labels"
VAL_IMAGES = BASE / "val" / "images"
VAL_LABELS = BASE / "val" / "labels"

EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}

# Images to hold out for validation (by number in the stop_XXX filename)
VAL_NUMBERS = list(range(1, 9)) + [64, 65]

images = sorted(
    [p for p in IMAGES.iterdir() if p.is_file() and p.suffix.lower() in EXTENSIONS]
)

print(f"Found {len(images)} images in data/images/")

missing = []
for img in images:
    label = LABELS / (img.stem + ".txt")
    if not label.exists():
        missing.append(img.name)
if missing:
    print(f"ERROR: {len(missing)} images have no label file. Annotate them first:")
    for name in missing:
        print(f"  - {name}")
    raise SystemExit(1)


def number_of(path):
    m = re.search(r"(\d+)", path.stem)
    return int(m.group(1)) if m else -1


val_imgs = [img for img in images if number_of(img) in VAL_NUMBERS]
train_imgs = [img for img in images if number_of(img) not in VAL_NUMBERS]

print(f"Validation images ({len(val_imgs)}): {[i.stem for i in val_imgs]}")


def clean_and_copy(items, dst_images, dst_labels):
    for d in (dst_images, dst_labels):
        if d.exists():
            for f in d.iterdir():
                f.unlink()
    for img in items:
        shutil.copy2(img, dst_images / img.name)
        shutil.copy2(LABELS / (img.stem + ".txt"), dst_labels / (img.stem + ".txt"))


clean_and_copy(train_imgs, TRAIN_IMAGES, TRAIN_LABELS)
clean_and_copy(val_imgs, VAL_IMAGES, VAL_LABELS)

print(f"Copied {len(train_imgs)} images+labels to train/")
print(f"Copied {len(val_imgs)} images+labels to val/")
print("Ready to train!")
