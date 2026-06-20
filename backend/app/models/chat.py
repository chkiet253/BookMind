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


class ResearchChat(Base):
    __tablename__ = "research_chats"

    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id    = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    book_id    = Column(UUID(as_uuid=True), ForeignKey("books.id"), nullable=False)
    messages   = Column(JSONB, nullable=False, default=list,
                        comment="[{ role, content, timestamp }]")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="research_chats")
    book = relationship("Book", back_populates="chats")

    __table_args__ = (
        Index("ix_research_chats_user_book", "user_id", "book_id"),
    )