from uuid import UUID
from psycopg import IntegrityError
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.config.exceptions.business_rule import BusinessRuleException
from app.models.detection import Detection


async def delete_user_detection(session: AsyncSession, id: str, user_id: UUID) -> bool:
    result = await session.execute(
        update(Detection)
        .where(
            Detection.id == id,
            Detection.deleted_at.is_(None),
            Detection.user_id == user_id,
        )
        .values(deleted_at=datetime.utcnow())
        .execution_options(synchronize_session=False)
    )

    try:
        await session.commit()

        return result.rowcount != 0
    except IntegrityError:
        await session.rollback()

        raise BusinessRuleException("Unable to delete detection")
