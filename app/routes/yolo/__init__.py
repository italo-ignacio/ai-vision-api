from fastapi import APIRouter

from .find import router as find_all_yolo

yolo_router = APIRouter(prefix="/yolo", tags=["Yolo"])

yolo_router.include_router(find_all_yolo)
