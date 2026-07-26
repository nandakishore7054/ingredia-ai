# 🤖 Computer Vision Scaling Architecture

This directory (`backend/ml/`) contains the professional infrastructure required to train and deploy custom object detection models for ingredient detection.

## 📁 Dataset Organization
To scale past onion/potato to 50+ ingredients, we have established a standard YOLO architecture:
- `dataset/train/`: Images and labels used to train the model.
- `dataset/valid/`: Images and labels used to test the model during training to prevent overfitting.
- `dataset/test/`: Images used for final accuracy evaluation.

Images go in `images/` subfolders, and YOLO `.txt` labels go in `labels/` subfolders.

## 🛠️ How to Train Custom Models
When you are ready to expand the model to recognize new ingredients (like tomatoes, chicken, broccoli):

1. **Annotate**: Upload your images to Roboflow, draw bounding boxes around the ingredients, and export the dataset in **YOLOv8 format**.
2. **Extract**: Place the exported `train`, `valid`, and `test` folders directly into `backend/ml/dataset/`.
3. **Configure**: Open `data.yaml` and ensure all your class names (ingredients) are listed correctly.
4. **Train**:
   Run the local training script:
   ```bash
   pip install ultralytics
   python train_yolo.py --epochs 100 --batch 16
   ```
5. **Deploy**: Once training completes, take the file located at `runs/ingredient_detection/weights/best.pt` and replace the hosted model string in `backend/app/services/yolo_service.py` with this local file path.

## 📈 Future Proofing
This architecture ensures we are not locked into cloud APIs. By using Ultralytics, we can train locally on an RTX GPU, or zip this folder and drop it directly into Google Colab for free T4 GPU training.
