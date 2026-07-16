import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Float, Integer, Text, Boolean,
    DateTime, ForeignKey, ARRAY, Index
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.base import Base


class SearchSession(Base):
    __tablename__ = "search_sessions"

    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id         = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True,
                             comment="Nullable — guest user vẫn search được")
    raw_query       = Column(Text, nullable=False)
    parsed_intent   = Column(JSONB, comment="{ genres, mood, pages_range, language }")
    result_book_ids = Column(ARRAY(UUID(as_uuid=True)), default=list,
                             comment="Top 5 book IDs trả về")
    created_at      = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="search_sessions")

    __table_args__ = (
        Index("ix_search_sessions_user_id", "user_id"),
        Index("ix_search_sessions_created_at", "created_at"),
    )


class UserInteraction(Base):
    __tablename__ = "user_interactions"

    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id    = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    book_id    = Column(UUID(as_uuid=True), ForeignKey("books.id"), nullable=False)
    action     = Column(String, nullable=False,
                        comment="view_detail | click_buy | save | skip | rate")
    rating     = Column(Float, comment="Chỉ có khi action=rate, 1.0–5.0")
    metadata   = Column(JSONB, default=dict,
                        comment="{ position_in_list, time_spent_ms, referrer }")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="interactions")
    book = relationship("Book", back_populates="interactions")

    __table_args__ = (
        Index("ix_user_interactions_user_book", "user_id", "book_id"),
        Index("ix_user_interactions_action", "action"),
        Index("ix_user_interactions_created_at", "created_at"),
    )
