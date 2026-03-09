from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.exceptions.business_rule import BusinessRuleException
from app.models.detection import Detection


async def add_detections(session: AsyncSession, detections_data: list[dict]):
    models = [
        Detection(
            image_path=d["image_path"],
            image_result_path=d["image_result_path"],
            result=d["result"],
            user_id=d["user_id"],
            yolo_id=d["yolo_id"],
        )
        for d in detections_data
    ]

    try:
        session.add_all(models)
        await session.commit()

        return models
    except IntegrityError:
        await session.rollback()

        raise BusinessRuleException("Unable to create detections")
