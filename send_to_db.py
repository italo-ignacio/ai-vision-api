import asyncio
import os
import shutil
from psycopg import IntegrityError
import yaml
from app.models.yolo import Yolo
from app.services.database import async_session
from app.services.azure_blob import blob_service

VERSION = "v8x"
TRAIN_NUMBER = None

RUNS_PATH = f"yolo/{VERSION}/runs/detect"


train_folders = [
    f for f in os.listdir(f"yolo/{VERSION}/runs/detect") if f.startswith("train")
]

if TRAIN_NUMBER:
    train = f"train{TRAIN_NUMBER}"
else:
    train = sorted(
        train_folders,
        key=lambda x: os.path.getmtime(os.path.join(f"yolo/{VERSION}/runs/detect", x)),
        reverse=True,
    )[0]


def extract_yolo_training_data(train_dir: str):
    shutil.copy(f"{train_dir}/weights/best.pt", f"app/yolo/yolo{VERSION}.pt")

    args_yaml = os.path.join(train_dir, "args.yaml")
    with open(args_yaml, "r") as f:
        args = yaml.safe_load(f)
    args.pop("save_dir", None)

    images = []

    def add_image(local_name: str, display: str):
        image_path = os.path.join(train_dir, local_name)

        if os.path.exists(image_path):
            url = blob_service.upload_image(image_path, "yolo-model/images")
            images.append({"name": display, "url": url})

    add_image("results.png", "Results")
    add_image("BoxF1_curve.png", "BoxF1 Curve")
    add_image("BoxP_curve.png", "BoxP Curve")
    add_image("BoxPR_curve.png", "BoxPR Curve")
    add_image("BoxR_curve.png", "BoxR Curve")
    add_image("confusion_matrix.png", "Confusion Matrix")
    add_image("confusion_matrix_normalized.png", "Confusion Matrix Normalized")
    add_image("labels.jpg", "Labels")

    results_csv = os.path.join(train_dir, "results.csv")
    if os.path.exists(results_csv):
        results_csv_path = blob_service.upload_image(results_csv, "yolo-model/csv")
    else:
        results_csv_path = None

    return {
        "name": f"Yolo {VERSION}",
        "path": f"yolo{VERSION}.pt",
        "csv_path": results_csv_path,
        "args": args,
        "images": images,
    }


def count_images(directory: str) -> int:
    if not os.path.exists(directory) or not os.path.isdir(directory):
        return 0

    exts = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"}
    total = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file.lower())[1] in exts:
                total += 1

    return total


async def save_yolo_model(train_dir: str):
    if os.path.exists(f"app/yolo/yolo{VERSION}.pt"):
        os.remove(f"app/yolo/yolo{VERSION}.pt")

    data = extract_yolo_training_data(train_dir)

    base_path = "yolo/dataset-base"

    train_count = count_images(os.path.join(base_path, "train", "images"))
    val_count = count_images(os.path.join(base_path, "val", "images"))
    test_count = count_images(os.path.join(base_path, "test", "images"))

    async with async_session() as session:
        new_yolo = Yolo(
            name=data["name"],
            path=data["path"],
            csv_path=data["csv_path"],
            args=data["args"],
            images=data["images"],
            total_train_images=train_count,
            total_val_images=val_count,
            total_test_images=test_count,
        )

        try:
            session.add(new_yolo)
            await session.commit()
        except IntegrityError:
            await session.rollback()


async def main():
    await save_yolo_model(f"{RUNS_PATH}/{train}")


asyncio.run(main())
