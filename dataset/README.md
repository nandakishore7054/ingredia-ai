# NutriVision AI — Computer Vision Ingredient Dataset

## Overview
This dataset contains custom ingredient images captured and annotated for training object detection models to identify raw cooking ingredients (vegetables, fruits, dairy, proteins, grains, and spices).

## Dataset Metadata
- **Version:** v1.0
- **Format:** YOLOv8 PyTorch / Text Bounding Box Annotations
- **Source:** Custom photos captured across various kitchen and lighting conditions
- **Annotation Tool:** Roboflow Annotate
- **Extensible Schema:** Designed to easily accommodate new ingredient categories over time.

## Dataset Structure
```
dataset/
├── data.yaml           # Class mappings & dataset configuration
├── README.md           # Dataset documentation
├── train/              # Training set (70%)
│   ├── images/
│   └── labels/
├── valid/              # Validation set (20%)
│   ├── images/
│   └── labels/
└── test/               # Test set (10%)
    ├── images/
    └── labels/
```

## Classes & Categories
The dataset currently tracks 25 core ingredient categories:
- **Vegetables:** Onion, Tomato, Potato, Carrot, Capsicum, Bell Pepper, Spinach, Chili
- **Dairy & Proteins:** Milk, Cheese, Paneer, Butter, Egg, Chicken, Lentils
- **Grains & Pantry:** Rice, Bread, Pasta, Turmeric, Oregano, Garlic, Ginger, Lemon, Apple, Banana

## Roboflow Preprocessing & Augmentations
- **Auto-Orient:** Strips EXIF orientation tags
- **Resize:** Stretched to 640x640 resolution
- **Augmentations:**
  - Random Rotation: ±15°
  - Random Brightness: ±25%
  - Horizontal Flip
