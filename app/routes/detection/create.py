from uuid import UUID
from fastapi import APIRouter, Depends
from requests import Session
from app.config.utils.current_user import get_current_user
from app.config.utils.format_detections import format_detections
from app.config.utils.section import get_section
from app.models.detection import Detection
from fastapi import UploadFile, File, Form
from typing import List
from app.models.yolo import Yolo
from app.repositories.detection.add import add_detections
from app.repositories.yolo.find import find_yolo
from app.yolo.run_detection import run_yolo_detection
from app.services.azure_blob import blob_service

router = APIRouter()


@router.post("/")
async def create_detection(
    current_user: Detection = Depends(get_current_user),
    session: Session = Depends(get_section),
    images: List[UploadFile] = File(...),
    yolo_ids: List[str] = Form(...),
):
    yolo_list = await find_yolo(session, yolo_ids)
    yolo_dict = {y.id: y for y in yolo_list["content"]}
    results = []

    async def stream_generator():
        image_batches = []

        for img in images:
            image_url = blob_service.upload_image(img, f"{current_user.id}/images")
            image_batches.append(image_url)

        for yolo_id in yolo_ids:
            yolo_item: Yolo = yolo_dict.get(UUID(yolo_id))

            if not yolo_item:
                continue

            detections_results = await run_yolo_detection(
                image_batches, yolo_item, f"{current_user.id}/results"
            )

            detections_data = format_detections(detections_results, current_user.id)
            detections = await add_detections(session, detections_data)

            results.append(
                {
                    "yolo_id": yolo_item.id,
                    "yolo_name": yolo_item.name,
                    "results": detections,
                }
            )
            # yield (json.dumps(detection_result) + "\n")

            # await asyncio.sleep(0)

    await stream_generator()

    return results
    # yield "__end__\n"

    # return StreamingResponse(stream_generator(), media_type="application/json")
