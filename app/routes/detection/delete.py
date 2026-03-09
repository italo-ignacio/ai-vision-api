from uuid import UUID
from fastapi import APIRouter, Depends
from requests import Session
from app.config.exceptions.not_found import NotFoundException
from app.config.utils.section import get_section
from app.models.detection import Detection
from app.repositories.detection.delete import delete_user_detection
from app.config.utils.current_user import get_current_user

router = APIRouter()


@router.delete("/{id}")
async def delete_detection(
    id: UUID,
    current_user: Detection = Depends(get_current_user),
    session: Session = Depends(get_section),
):
    detection = await delete_user_detection(session, id, current_user.id)

    if not detection:
        raise NotFoundException("Detection")

    return {"detail": "Successfully deleted"}
