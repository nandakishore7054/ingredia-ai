import argparse
from ultralytics import YOLO

def train_model(epochs: int = 50, batch_size: int = 16, imgsz: int = 640):
    """
    Trains a custom YOLOv8 model using the data.yaml configuration.
    This script is designed for local training or execution on Google Colab.
    """
    print("--- Starting YOLOv8 Training Pipeline ---")
    
    # Initialize the nano model (fastest, great for mobile/web apps)
    model = YOLO("yolov8n.pt") 
    
    # Train the model
    results = model.train(
        data="data.yaml",
        epochs=epochs,
        batch=batch_size,
        imgsz=imgsz,
        project="runs",
        name="ingredient_detection",
        exist_ok=True
    )
    
    print("\n--- Training Complete ---")
    print("Best weights saved at: runs/ingredient_detection/weights/best.pt")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train YOLOv8 on Custom Ingredient Dataset")
    parser.add_argument("--epochs", type=int, default=50, help="Number of training epochs")
    parser.add_argument("--batch", type=int, default=16, help="Batch size")
    parser.add_argument("--imgsz", type=int, default=640, help="Image size (e.g. 640)")
    
    args = parser.parse_args()
    train_model(epochs=args.epochs, batch_size=args.batch, imgsz=args.imgsz)
