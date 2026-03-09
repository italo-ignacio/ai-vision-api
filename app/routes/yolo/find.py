from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from requests import Session
from app.config.utils.current_user import get_current_user
from app.config.utils.section import get_section
from app.models.user import User
from app.repositories.yolo.find import find_yolo

router = APIRouter()


class YoloFilter(BaseModel):
    ids: Optional[List[UUID]] = None


@router.get("/")
async def find_all_yolo(
    filters: YoloFilter = Depends(),
    session: Session = Depends(get_section),
    _: User = Depends(get_current_user),
):
    response = await find_yolo(session, filters.ids)

    return response
