from psycopg import IntegrityError
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.config.exceptions.business_rule import BusinessRuleException
from app.models.user import User


async def delete_account(session: AsyncSession, id: str) -> User | None:
    result = await session.execute(
        update(User)
        .where(User.id == id, User.deleted_at.is_(None))
        .values(deleted_at=datetime.utcnow())
        .execution_options(synchronize_session=False)
    )

    try:
        await session.commit()

        return result.rowcount != 0
    except IntegrityError:
        await session.rollback()

        raise BusinessRuleException("Failed to delete account")
