from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from requests import Session
from app.config.utils.current_user import get_current_user
from app.config.utils.section import get_section
from app.models.user import User
from app.repositories.detection.find import find_detection

router = APIRouter()


class DetectionFilter(BaseModel):
    page: int = 1
    limit: int = 15
    success: Optional[bool] = None
    yolo_ids: Optional[str] = None


@router.get("/")
async def find_all_detection(
    filters: DetectionFilter = Depends(),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_section),
):
    data = filters.model_dump()

    if data["yolo_ids"]:
        data["yolo_ids"] = data["yolo_ids"].split(",")

    response = await find_detection(
        session,
        **data,
        user_id=current_user.id,
    )

    return response
