import uuid
from datetime import datetime
from sqlalchemy import Column, Index, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import deferred, relationship
from app.services.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False, index=True)
    hashed_password = deferred(Column(String, nullable=False))

    detections = relationship("Detection", back_populates="user")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    __table_args__ = (
        Index(
            "unique_username_deleted_at_null",
            "username",
            unique=True,
            postgresql_where=(deleted_at.is_(None)),
        ),
    )
