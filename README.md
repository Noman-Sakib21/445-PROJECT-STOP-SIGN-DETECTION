# Stop Sign Detection in Street Images

A YOLOv8-based computer vision project that detects stop signs in street photographs.
The model was trained **from scratch** (no pre-trained weights) on a custom dataset of
65 manually annotated street images collected for this CSE445 semester project.

## Features

- Single-class object detector (`stop_sign`) built with Ultralytics YOLOv8n
- Trained from random weights entirely on our own annotated dataset
- Runs on CPU (no GPU required), ~50 ms per image at 640×640
- Easy one-command usage via `main.py`
- One-click test tool: double-click `test_photo.bat` and pick any photo

## How to Run

### 1. Install dependencies

Requires Python 3.10+. Create a virtual environment and install packages:

```bash
python -m venv venv
venv\Scripts\activate              # Windows
pip install -r requirements.txt    # note: installs CPU PyTorch
```

### 2. Run the project

```bash
python main.py                          # runs on the validation dataset
python main.py photo.jpg                # detect on a single image
python main.py C:\path\to\images        # detect on a whole folder
```

Annotated images (red bounding boxes + confidence) are saved to `runs\detections\`.

### One-click tester (Windows)

Double-click **`test_photo.bat`** and choose an image from the file picker, or drag an
image directly onto the `.bat` icon. No typing required.

## Repository Structure

```
├── main.py                  # entry point: run the detection pipeline
├── README.md
├── requirements.txt         # required Python libraries
├── data/                    # dataset (images + YOLO labels, train/val split)
├── support/                 # helper code (training, conversion, split, tester)
├── models/                  # trained model weights (stop_sign_detector.pt)
└── others/                  # reports, presentations, and demo video
```

## Dataset

- 65 street images collected from the web, varied angles/lighting/distances
- Manually annotated with labelme (tight bounding box per image)
- Converted to YOLO format by `support/convert_labelme_to_yolo.py`
- Split: **55 train / 10 validation** (`stop_001`–`stop_008`, `stop_064`, `stop_065`) —
  verified programmatically to have zero overlap

## Model Performance (held-out validation set)

| Metric | Value |
|---|---|
| Precision | 0.957 |
| Recall | 1.000 |
| F1 Score | 0.978 |
| mAP50 | 0.995 |
| mAP50-95 | 0.712 |
| Per-image accuracy | 10/10 validation images detected correctly |

Training: 214 epochs from scratch, early-stopped (patience=40), 640×640, CPU (~61 min).
Best checkpoint at epoch 180.

## Requirements

See `requirements.txt`. Key packages: PyTorch 2.13 (CPU), Ultralytics 8.4.115,
OpenCV 5.0, NumPy, PyYAML, Matplotlib.

## Authors

- Noman Sakib — 2232399642
- Md. Samin Islam — 2233401642
- Saymon Feroz Sadaf — 2312672042
- Ishmam Islam Bhuiyan — 2014331042

*CSE445, Section 7 — Semester Project (Group 8)*