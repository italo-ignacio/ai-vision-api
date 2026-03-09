import os
import shutil

DATASET_BASE = "dataset-base"

VERSION = "v11s"


os.makedirs(VERSION, exist_ok=True)

shutil.copy(f"{DATASET_BASE}/data.yaml", f"{VERSION}/data.yaml")

dst = f"{VERSION}/train.py"
shutil.copy(f"{DATASET_BASE}/train.py", dst)

with open(dst, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("yolo", f"yolo{VERSION}")

with open(dst, "w", encoding="utf-8") as f:
    f.write(content)

print("Dataset organizado!")
