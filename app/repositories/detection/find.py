from typing import Optional
from uuid import UUID
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.utils.pagination import paginate
from app.models.detection import Detection


class FindDetectionResponse:
    content: list[Detection]
    page: int
    limit: int
    total_elements: int
    total_pages: int


async def find_detection(
    session: AsyncSession,
    user_id: UUID,
    page: int,
    limit: int,
    success: Optional[bool],
    yolo_ids: Optional[list[str]],
) -> FindDetectionResponse:
    query = (
        select(Detection)
        .where(
            Detection.deleted_at.is_(None),
            Detection.user_id == user_id,
        )
        .order_by(Detection.created_at.desc())
    )

    if success is not None:
        query = query.where(Detection.success == success)

    print(yolo_ids)
    if yolo_ids:
        query = query.where(
            Detection.yolo_id.in_([UUID(yolo_id) for yolo_id in yolo_ids])
        )

    return await paginate(session, query, page, limit)
