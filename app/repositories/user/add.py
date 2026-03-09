from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.exceptions.business_rule import BusinessRuleException
from app.config.utils.password import get_password_hash
from app.models.user import User


async def add_user(session: AsyncSession, username: str, password: str) -> User:
    hashed_password = get_password_hash(password)

    user = User(
        username=username,
        hashed_password=hashed_password,
    )

    session.add(user)

    try:
        await session.commit()
        await session.refresh(user)

        return user
    except IntegrityError:
        await session.rollback()

        raise BusinessRuleException("Unable to create user")
