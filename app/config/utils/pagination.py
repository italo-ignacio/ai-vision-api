from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession


async def paginate(
    session: AsyncSession,
    query,
    page: int = 1,
    limit: int = 10,
):
    if page < 1:
        page = 1

    if limit < 1:
        limit = 10
    elif limit > 50:
        limit = 50

    count_query = select(func.count()).select_from(query.subquery())
    total_elements = (await session.execute(count_query)).scalar()

    offset = (page - 1) * limit

    query = query.offset(offset).limit(limit)

    result = await session.execute(query)
    content = result.scalars().all()

    total_pages = (total_elements + limit - 1) // limit

    return {
        "content": content,
        "page": page,
        "limit": limit,
        "total_elements": total_elements,
        "total_pages": total_pages,
    }
