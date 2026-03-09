from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User


async def find_user_by_id(session: AsyncSession, id: str) -> User | None:
    result = await session.execute(
        select(User).where(User.id == id, User.deleted_at.is_(None))
    )

    return result.scalar_one_or_none()
