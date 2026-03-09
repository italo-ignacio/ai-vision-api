import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.services.database import Base


class Yolo(Base):
    __tablename__ = "yolo"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    path = Column(String, nullable=False)
    csv_path = Column(String, nullable=True)
    args = Column(JSONB, nullable=True)
    images = Column(JSONB, nullable=True)

    total_train_images = Column(Integer, nullable=False)
    total_val_images = Column(Integer, nullable=False)
    total_test_images = Column(Integer, nullable=False)

    detections = relationship("Detection", back_populates="yolo")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
