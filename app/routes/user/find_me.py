from fastapi import APIRouter, Depends
from app.config.utils.current_user import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/me")
async def find_me(current_user: User = Depends(get_current_user)):
    return current_user
