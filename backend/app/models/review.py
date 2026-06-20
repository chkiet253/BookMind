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

class Review(Base):
    __tablename__ = "reviews"

    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    book_id         = Column(UUID(as_uuid=True), ForeignKey("books.id"), nullable=False)
    source          = Column(String, nullable=False, comment="tiki | fahasa | goodreads")
    source_url      = Column(String)
    reviewer_name   = Column(String)
    content         = Column(Text, nullable=False)
    sentiment_score = Column(Float, comment="-1.0 đến 1.0")
    like_count      = Column(Integer, default=0)
    published_at    = Column(DateTime(timezone=True))
    scraped_at      = Column(DateTime(timezone=True), server_default=func.now())

    book = relationship("Book", back_populates="reviews")

    __table_args__ = (
        Index("ix_reviews_book_sentiment", "book_id", "sentiment_score"),
        Index("ix_reviews_book_source", "book_id", "source"),
    )


class Quote(Base):
    __tablename__ = "quotes"

    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    book_id    = Column(UUID(as_uuid=True), ForeignKey("books.id"), nullable=False)
    content    = Column(Text, nullable=False)
    source_url = Column(String, comment="Goodreads / Wikiquote")
    scraped_at = Column(DateTime(timezone=True), server_default=func.now())

    book = relationship("Book", back_populates="quotes")

    __table_args__ = (
        Index("ix_quotes_book_id", "book_id"),
    )
