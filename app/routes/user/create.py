from fastapi import APIRouter, Depends
from pydantic import BaseModel
from requests import Session
from app.config.utils.section import get_section
from app.repositories.user.add import add_user

router = APIRouter()


class InsertUserRequest(BaseModel):
    username: str
    password: str


@router.post("/")
async def create_user(
    request: InsertUserRequest,
    session: Session = Depends(get_section),
):
    await add_user(session, request.username, request.password)

    return {"detail": "Successfully created"}
