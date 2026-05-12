import uuid
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=False)
    password = Column(String)
    tier = Column(String)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
