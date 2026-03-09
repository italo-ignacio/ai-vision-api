from fastapi import APIRouter

from .create import router as create_detection
from .delete import router as delete_detection
from .find import router as find_all_detection
from .find_one import router as find_one_detection
from .update_success import router as update_user_success

detection_router = APIRouter(prefix="/detection", tags=["Detection"])

detection_router.include_router(create_detection)
detection_router.include_router(delete_detection)
detection_router.include_router(find_one_detection)
detection_router.include_router(find_all_detection)
detection_router.include_router(update_user_success)
