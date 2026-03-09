from fastapi import APIRouter, Depends
from pydantic import BaseModel
from requests import Session
from app.config.exceptions.unauthorized import UnauthorizedException
from app.config.utils.jwt_handler import create_token
from app.config.utils.password import verify_password
from app.config.utils.section import get_section
from app.repositories.user.find_by_username import find_user_by_username

router = APIRouter(tags=["Auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
async def login(
    request: LoginRequest,
    session: Session = Depends(get_section),
):
    user = await find_user_by_username(session, request.username)

    if not user or not verify_password(request.password, user.hashed_password):
        raise UnauthorizedException("Invalid username and/or password")

    token = create_token({"sub": str(user.id), "username": user.username})

    return {
        "access_token": token,
        "user": {
            "id": str(user.id),
            "username": user.username,
            "created_at": user.created_at,
        },
    }
