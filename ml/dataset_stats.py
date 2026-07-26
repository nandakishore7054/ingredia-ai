"""
Dataset Summary Utility
========================
Scans the dataset/ directory and displays statistics on images, labels,
and class distributions defined in data.yaml.
"""

import os
import yaml

def analyze_dataset(dataset_dir="../dataset"):
    yaml_path = os.path.join(dataset_dir, "data.yaml")
    if not os.path.exists(yaml_path):
        print(f"data.yaml not found at {yaml_path}")
        return

    with open(yaml_path, "r") as f:
        data_config = yaml.safe_load(f)

    classes = data_config.get("names", [])
    print("=" * 50)
    print("NutriVision AI — Dataset Summary")
    print("=" * 50)
    print(f"Total Classes Defined: {len(classes)}")
    print(f"Class Names: {', '.join(classes)}")
    print("-" * 50)

    for split in ["train", "valid", "test"]:
        split_dir = os.path.join(dataset_dir, split, "images")
        if os.path.exists(split_dir):
            images = [f for f in os.listdir(split_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
            print(f"Split [{split.upper()}]: {len(images)} images")
        else:
            print(f"Split [{split.upper()}]: Directory not created yet ({split_dir})")
    print("=" * 50)

if __name__ == "__main__":
    analyze_dataset()
