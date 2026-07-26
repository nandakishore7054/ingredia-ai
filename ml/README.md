# Machine Learning Lifecycle & Training Documentation

## 1. Computer Vision Pipeline Architecture

NutriVision AI implements an end-to-end Machine Learning lifecycle for ingredient detection:

```
[ Dataset Curation ] ──> [ Roboflow Annotation ] ──> [ Augmentation & Training ] 
                                                                │
[ Recipe Matching Engine ] <── [ Roboflow Hosted API ] <───────┘
```

## 2. Dataset Curation & Annotation
- **Data Collection:** Images captured across various lighting conditions, kitchen environments, and arrangements (singly and grouped).
- **Bounding Box Annotation:** Annotated using Roboflow Annotate in YOLO normalized format `[class_id, x_center, y_center, width, height]`.
- **Split Ratio:** 70% Train / 20% Validation / 10% Test.

## 3. Training Workflow (Roboflow Hosted Train)
- **Base Architecture:** YOLOv8 Nano / Small for real-time inference efficiency.
- **Input Resolution:** 640 x 640 pixels.
- **Preprocessing:** EXIF auto-orientation, static resizing.
- **Augmentation Strategy:** Random rotation (±15°), brightness adjustment (±25%), horizontal flips to prevent overfitting on small sample counts.

## 4. Deployment & Production Inference
- Model trained and hosted on **Roboflow Serverless Infrastructure**.
- The FastAPI backend communicates via REST API in `backend/app/services/roboflow_service.py`.
- Detections above a confidence threshold of `0.40` are extracted with normalized bounding box coordinates and mapped to the database ingredient catalog.
