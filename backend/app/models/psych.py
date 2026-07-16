import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Float, Integer, Text, Boolean,
    DateTime, ForeignKey, ARRAY, Index
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func
from models.base import Base

class PsychTestResult(Base):
    __tablename__ = "psych_test_results"

    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id    = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    test_level = Column(String, nullable=False, comment="quick | standard | deep")
    answers    = Column(JSONB, nullable=False, comment="Raw câu trả lời theo từng câu hỏi")
    scores     = Column(JSONB, nullable=False,
                        comment='{ big5: {...}, mbti: "INFP", reading_style: "..." }')
    taken_at   = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="psych_test_results")

    __table_args__ = (
        Index("ix_psych_test_results_user_id", "user_id"),
    )