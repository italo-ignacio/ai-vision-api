from uuid import UUID
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.detection import Detection


async def find_detection_by_id(
    session: AsyncSession, id: str, user_id: UUID
) -> Detection | None:
    result = await session.execute(
        select(Detection).where(
            Detection.id == id,
            Detection.deleted_at.is_(None),
            Detection.user_id == user_id,
        )
    )

    return result.scalar_one_or_none()
