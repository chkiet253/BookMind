import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Float, Integer, Text, Boolean,
    DateTime, ForeignKey, ARRAY, Index
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import  relationship
from sqlalchemy.sql import func
from models.base import Base

class User(Base):
    __tablename__ = "users"

    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email           = Column(String, unique=True, nullable=False)
    name            = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    avatar_url      = Column(String)
    profile_vector  = Column(JSONB, default=dict,
                             comment="Embedding vector cập nhật liên tục từ behavior")
    psych_scores    = Column(JSONB, default=dict,
                             comment="{ openness, conscientiousness, extraversion, agreeableness, neuroticism, mbti }")
    created_at      = Column(DateTime(timezone=True), server_default=func.now())
    updated_at      = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relations
    search_sessions    = relationship("SearchSession", back_populates="user", lazy="dynamic")
    interactions       = relationship("UserInteraction", back_populates="user", lazy="dynamic")
    research_chats     = relationship("ResearchChat", back_populates="user", lazy="dynamic")
    psych_test_results = relationship("PsychTestResult", back_populates="user", lazy="dynamic")