import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db import Base

class Clan(Base):
    __tablename__ = "clans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    name = Column(String, nullable=False)
    region = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())