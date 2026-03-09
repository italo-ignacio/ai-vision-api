from fastapi import APIRouter
from .create import router as create_user
from .find_me import router as find_me_route
from .delete_me import router as delete_me_route

user_router = APIRouter(prefix="/user", tags=["User"])

user_router.include_router(create_user)
user_router.include_router(find_me_route)
user_router.include_router(delete_me_route)
