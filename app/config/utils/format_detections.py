def format_detections(result: dict, user_id: str):
    formatted_detections = []

    for detection in result["results"]:
        formatted_detections.append(
            {
                "image_path": detection["image_path"],
                "image_result_path": detection["image_result_path"],
                "user_id": user_id,
                "yolo_id": result["yolo_id"],
                "result": {
                    "yolo_id": str(result["yolo_id"]),
                    "yolo_name": result["yolo_name"],
                    "yolo_path": result["yolo_path"],
                    "detected_objects": detection["detected_objects"],
                    "speed": detection["speed"],
                },
            }
        )

    return formatted_detections
