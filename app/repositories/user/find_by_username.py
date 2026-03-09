from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import undefer
from app.models.user import User


async def find_user_by_username(session: AsyncSession, username: str) -> User | None:
    result = await session.execute(
        select(User)
        .where(User.username == username, User.deleted_at.is_(None))
        .options(undefer(User.hashed_password))
    )

    return result.scalar_one_or_none()
