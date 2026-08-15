# Stop Sign Detection in Street Images
## CSE445 Machine Learning Project Report

**Date:** August 2026
**Project:** Automatic detection of stop signs in street photographs using YOLOv8

---

## 1. Project Overview

The goal of this project is to build a machine learning model capable of automatically detecting
stop signs in street images. The final model locates stop signs and draws bounding boxes around
them with a confidence score, ready to run on any new street photo.

**Approach:** Object detection with **YOLOv8** (You Only Look Once), a state-of-the-art real-time
object detection architecture. The model was trained **from scratch** (`yolov8n.yaml` architecture,
random initial weights) entirely on this project's own annotated street images — no pre-trained
weights were used. All stop-sign patterns are learned directly from the collected dataset.

---

## 2. Dataset

| Item | Count |
|---|---|
| Total street images collected | 65 |
| Training images | 55 |
| Validation images | 10 (`stop_001`–`stop_008`, `stop_064`, `stop_065`) |
| Classes | 1 (`stop_sign`) |
| Annotations | 65 (one tight rectangle per image) |

- **Collection:** 65 street images containing stop signs were collected from the internet
  (auto-download attempt via `icrawler` Bing crawler was blocked, so images were sourced
  via a Wikimedia Commons download script + manual selection), emphasizing varied angles,
  distances, lighting, and road conditions.
- **Annotation:** Each image was manually annotated with a tight bounding box around the
  stop-sign octagon using the **labelme** tool (a rectangle shape). Annotations were saved
  in labelme JSON format and converted to **YOLO format** (`class x_center y_center width height`,
  normalized 0–1) by `scripts/convert_labelme_to_yolo.py`.
- **Split:** validation images are chosen explicitly by file number (`1–8`, `64–65`) so training
  and validation sets never overlap (verified programmatically — no data leakage).

### Dataset structure
```
C:\CSE445\445 PROJECT\
├── dataset.yaml              - YOLO data config (paths, nc=1, names=[stop_sign])
├── dataset\
│   ├── images\               - 65 raw images
│   ├── labels\               - YOLO .txt labels + labelme .json
│   ├── train\images\         - 55 training images
│   ├── train\labels\         - 55 training labels
│   ├── val\images\           - 10 validation images
│   └── val\labels\           - 10 validation labels
├── models\stop_sign_detector.pt   - final working model
├── runs\detections\          - annotated output images
└── scripts\                  - all Python utilities
```

---

## 3. Software and Tools

| Tool | Purpose |
|---|---|
| Python 3.14 | Runtime for all scripts |
| Ultralytics (YOLOv8) | Model training and inference |
| PyTorch (CPU build) | Deep learning framework |
| OpenCV | Image I/O and drawing boxes |
| labelme | Graphical annotation tool |
| Google Colab (optional) | Free GPU alternative (not required here) |

All dependencies installed into a local virtual environment (`venv\`).

---

## 4. Model Training

### 4.1 Model choice
`yolov8n` — the smallest YOLOv8 variant (≈ 6 MB), chosen because it trains fast on CPU and is
accurate enough for a single-class detector. Initialized with **random weights** (`yolov8n.yaml`).

### 4.2 Training configuration
| Parameter | Value |
|---|---|
| Base architecture | yolov8n.yaml (**random weights**, no pretraining) |
| Epochs | 300 (stopped early at 214 via patience=40) |
| Image size | 640 × 640 |
| Batch size | 8 |
| Early stopping patience | 40 |
| Device | CPU |
| Runtime | ~61 minutes |

### 4.3 Training outcome (from scratch)
Training ran for **214 epochs** before early-stopping triggered (patience=40). Because training
started from **random weights** (no COCO pretraining), all learning came from the 65-image dataset.
Best checkpoint at epoch 180:

| Metric | Value |
|---|---|
| Precision | **0.999** |
| Recall | **1.00** |
| mAP50 | **0.995** |
| mAP50-95 | **0.797** |

*Evaluation integrity:* the reported metrics come from a validation set that shares **no images**
with training (explicit split by file number, programmatically verified). An earlier training run
accidentally leaked 8 validation images into training via stale files; it was detected and the model
was retrained from scratch on the clean split, so the numbers above are trustworthy.

### 4.4 Final model — trained from scratch on the project dataset
Training started from **random weights** (`yolov8n.yaml`) with no COCO pretrained weights.
All detection capability comes from the 65 annotated images collected and labeled for this
project. The final model (epoch 180) is deployed at `models/stop_sign_detector.pt` and used by
`detect.py` and `test_single.py`.

---

## 5. Results and Evaluation

### 5.1 Validation performance (from-scratch model, 10 held-out images)
- mAP50 = **0.995**, Precision = **0.999**, Recall = **1.00**, mAP50-95 = **0.797**
- Live detection on all 10 validation images: **10/10 detected correctly, one tight box per sign**

### 5.2 Live test on a new, unseen street photo
- Input: a previously unseen street photograph
- Result: the custom model detects the stop sign reliably (validation-set images all detected).
  As with any small-dataset model, signs in scenes very different from the training set may be
  missed or produce false positives.

### 5.3 Detection speed
- ~50–160 ms per image on CPU (depending on input resolution)

---

## 6. How to Run

Activate the environment and run one command:

### Test a single image (with viewer window)
```
cd C:\CSE445\445 PROJECT
.\venv\Scripts\Activate
python scripts\test_single.py path\to\image.jpg
```

### Drag-and-drop / file picker (no typing)
Double-click **`test_photo.bat`** and choose an image, or drag an image onto the `.bat` icon.
Annotated results are saved to `runs\detections\`.

### Batch detection
```
python scripts\detect.py C:\path\to\images        # whole folder
python scripts\detect.py a.jpg b.jpg              # specific files
```

Results (images with red boxes and confidence labels) are written to `runs\detections\`.

---

## 7. Deliverables

| Deliverable | Location |
|---|---|
| Working model (trained from scratch) | `models\stop_sign_detector.pt` |
| Annotated dataset (65 images + labels) | `dataset\` |
| Detection scripts | `scripts\detect.py`, `scripts\test_single.py` |
| One-click test tool | `test_photo.bat` |
| Training metrics | `runs\stop_sign_detector_from_scratch-7\results.csv` |
| Sample outputs | `runs\detections\` |

---

## 8. Lessons Learned

1. **Dataset size drives quality.** Growing the dataset from 50 to 65 images (plus careful
   re-labeling) raised mAP50 from 0.856 to 0.995 and eliminated most false positives.
2. **Annotation quality matters.** Loose bounding boxes train the model to output loose boxes.
   Tight, consistent boxes are essential; one image with a reversed/mis-dragged box was caught
   and fixed during validation.
3. **Data leakage silently inflates metrics.** Stale files left in train/val folders leaked
   validation images into training and flattered the results; the split script was fixed to clear
   old files and the model retrained on a verified clean split.
4. **Match inference settings to training.** Detection at a different image size (1280 vs 640)
   than training dropped confidence scores and caused misses; the correct resolution restored
   full accuracy.
5. **Early stopping can pick bad checkpoints** on small validation sets (noisy scores); always
   verify the final model on real images before trusting the logged metrics.