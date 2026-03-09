from uuid import UUID
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from requests import Session
from app.config.exceptions.not_found import NotFoundException
from app.config.utils.section import get_section
from app.models.detection import Detection
from app.config.utils.current_user import get_current_user
from app.repositories.detection.update_success import (
    update_user_detection_success,
)

router = APIRouter()


class UpdateDetectionSuccess(BaseModel):
    success: bool


@router.put("/{id}")
async def update_detection_success(
    request: UpdateDetectionSuccess,
    id: UUID,
    current_user: Detection = Depends(get_current_user),
    session: Session = Depends(get_section),
):
    detection = await update_user_detection_success(
        session, id, current_user.id, request.success
    )

    if not detection:
        raise NotFoundException("Detection")

    return {"detail": "Successfully updated"}
