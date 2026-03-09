from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from uuid import UUID
from requests import Session
from app.config.exceptions.unauthorized import UnauthorizedException
from app.config.utils.jwt_handler import verify_token
from app.config.utils.section import get_section
from app.repositories.user.find_by_id import find_user_by_id

bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: Session = Depends(get_section),
):
    token = credentials.credentials
    payload = verify_token(token)

    if not payload or "sub" not in payload:
        raise UnauthorizedException("Invalid token")

    user_id = UUID(payload["sub"])

    user = await find_user_by_id(session, user_id)

    if not user:
        raise UnauthorizedException("User not found")

    return user
