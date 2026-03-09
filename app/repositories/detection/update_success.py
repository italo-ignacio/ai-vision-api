from uuid import UUID
from psycopg import IntegrityError
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.exceptions.business_rule import BusinessRuleException
from app.models.detection import Detection


async def update_user_detection_success(
    session: AsyncSession, id: str, user_id: UUID, success: bool
) -> bool:
    result = await session.execute(
        update(Detection)
        .where(
            Detection.id == id,
            Detection.deleted_at.is_(None),
            Detection.user_id == user_id,
        )
        .values(success=success)
        .execution_options(synchronize_session=False)
    )

    try:
        await session.commit()

        return result.rowcount != 0
    except IntegrityError:
        await session.rollback()

        raise BusinessRuleException("Unable to Update detection")
