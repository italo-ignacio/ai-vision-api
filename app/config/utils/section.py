from app.services.database import async_session


async def get_section():
    async with async_session() as session:
        yield session
