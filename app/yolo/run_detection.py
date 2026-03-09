from ultralytics import YOLO
from app.config.utils.format_yolo_result import format_yolo_result
from app.models.yolo import Yolo


async def run_yolo_detection(list_of_images: list[str], yolo: Yolo, folder: str):
    model = YOLO(f"app/yolo/{yolo.path}")

    results = model.predict(list_of_images, save=True, name="results")

    return {
        "yolo_id": yolo.id,
        "yolo_name": yolo.name,
        "yolo_path": yolo.path,
        "results": format_yolo_result(results, folder, list_of_images),
    }
