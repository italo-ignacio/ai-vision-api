import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.services.database import Base


class Detection(Base):
    __tablename__ = "detections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    image_path = Column(String, nullable=False)
    image_result_path = Column(String, nullable=False)
    result = Column(JSONB, nullable=False)
    success = Column(Boolean, default=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="detections")

    yolo_id = Column(UUID(as_uuid=True), ForeignKey("yolo.id"), nullable=False)
    yolo = relationship("Yolo", back_populates="detections")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
