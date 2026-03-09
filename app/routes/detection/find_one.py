from uuid import UUID
from fastapi import APIRouter, Depends
from requests import Session
from app.config.exceptions.not_found import NotFoundException
from app.config.utils.section import get_section
from app.models.detection import Detection
from app.repositories.detection.find_by_id import find_detection_by_id
from app.config.utils.current_user import get_current_user

router = APIRouter()


@router.get("/{id}")
async def find_one_detection(
    id: UUID,
    current_user: Detection = Depends(get_current_user),
    session: Session = Depends(get_section),
):
    detection = await find_detection_by_id(session, id, current_user.id)

    if not detection:
        raise NotFoundException("Detection")

    return detection
