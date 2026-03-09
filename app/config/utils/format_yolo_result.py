import os
import shutil
from ultralytics.engine.results import Results
from app.services.azure_blob import blob_service


def format_yolo_result(results: list[Results], folder: str, list_of_images: list[str]):
    formatted_results = []

    for index, result in enumerate(results):
        image_path_result = os.path.join(result.save_dir, os.path.basename(result.path))

        result_path = blob_service.upload_image(image_path_result, folder)

        detected_objects = []

        for box in result.boxes:
            cls_id = int(box.cls[0])
            cls_name = result.names[cls_id]
            conf = float(box.conf[0])

            x, y, w, h = box.xywh[0].tolist()

            detected_objects.append(
                {
                    "class_id": cls_id,
                    "class_name": cls_name,
                    "confidence": conf,
                    "bbox": {"x": x, "y": y, "width": w, "height": h},
                }
            )

        if os.path.exists(image_path_result):
            os.remove(image_path_result)

        if os.path.isdir(result.save_dir):
            if not os.listdir(result.save_dir):
                shutil.rmtree(result.save_dir)

        formatted_results.append(
            {
                "image_path": list_of_images[index],
                "image_result_path": result_path,
                "detected_objects": detected_objects,
                "speed": {
                    "preprocess_ms": result.speed["preprocess"],
                    "inference_ms": result.speed["inference"],
                    "postprocess_ms": result.speed["postprocess"],
                    "total_ms": (
                        result.speed["preprocess"]
                        + result.speed["inference"]
                        + result.speed["postprocess"]
                    ),
                },
            }
        )

    return formatted_results
