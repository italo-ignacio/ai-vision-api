from typing import List, Optional
from uuid import UUID
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.yolo import Yolo
from sqlalchemy import func, cast, Integer, case


class FindYoloReturn:
    content: list[Yolo]


async def find_yolo(
    session: AsyncSession,
    ids: Optional[List[UUID]] = None,
) -> FindYoloReturn:
    query = (
        select(Yolo)
        .where(Yolo.deleted_at.is_(None))
        .order_by(
            cast(func.regexp_replace(Yolo.name, r"[^0-9]", "", "g"), Integer),
            case(
                (func.right(Yolo.name, 1) == "n", 1),
                (func.right(Yolo.name, 1) == "s", 2),
                (func.right(Yolo.name, 1) == "m", 3),
                (func.right(Yolo.name, 1) == "l", 4),
                (func.right(Yolo.name, 1) == "x", 5),
                else_=99,
            ),
        )
    )

    if ids:
        query = query.where(Yolo.id.in_(ids))

    result = await session.execute(query)
    content = result.scalars().all()

    return {"content": content}
