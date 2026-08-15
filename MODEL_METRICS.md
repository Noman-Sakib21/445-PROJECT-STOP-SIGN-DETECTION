# Stop Sign Detection — Model Metrics

**Model:** `models/stop_sign_detector.pt` (YOLOv8n, trained from scratch)
**Evaluation:** 10 held-out validation images (`stop_001`-`stop_008`, `stop_064`, `stop_065`)
**Best checkpoint:** epoch 180 of 214

## Final Metrics

| Metric | Value |
|---|---|
| Precision | **0.957** |
| Recall | **1.000** |
| F1 Score | **0.978** |
| mAP50 | **0.995** |
| mAP50-95 | **0.712** |
| Accuracy | 100% (10/10 validation images detected correctly) |

## Notes

- **F1 Score** is computed as `2 * (Precision * Recall) / (Precision + Recall)`.
- **Accuracy** here is per-image: all 10/10 held-out validation images were detected with exactly
  one correct bounding box. (In object detection, mAP is the standard accuracy measure; accuracy
  is reported as a supplementary per-image result.)
- Metrics recorded from `runs/stop_sign_detector_from_scratch-7/results.csv` (best epoch).
- Precision/Recall can vary slightly between runs (e.g. 0.90–0.96) because the small validation
  set and random test-time augmentation make the scores noisy.

## Derived from

- Dataset: 65 images (55 train / 10 val), no overlap
- Training: 300 epochs cap, early-stopped at 214 (patience=40), 640x640, CPU, ~61 min
