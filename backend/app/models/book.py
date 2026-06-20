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

class Book(Base):
    __tablename__ = "books"

    id           = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title        = Column(String, nullable=False)
    author       = Column(String, nullable=False)
    isbn         = Column(String, unique=True)
    publisher    = Column(String)
    pages        = Column(Integer)
    year         = Column(Integer)
    language     = Column(String, default="vi")
    genres       = Column(ARRAY(String), default=list,
                          comment='Array: ["trinh thám", "tâm lý"]')
    cover_url    = Column(String)
    avg_rating   = Column(Float)
    review_count = Column(Integer, default=0)
    tiki_url     = Column(String)
    fahasa_url   = Column(String)
    goodreads_url= Column(String)
    scraped_at   = Column(DateTime(timezone=True))
    created_at   = Column(DateTime(timezone=True), server_default=func.now())

    # Relations
    reviews      = relationship("Review", back_populates="book", lazy="dynamic")
    quotes       = relationship("Quote", back_populates="book", lazy="dynamic")
    interactions = relationship("UserInteraction", back_populates="book", lazy="dynamic")
    chats        = relationship("ResearchChat", back_populates="book", lazy="dynamic")

    __table_args__ = (
        Index("ix_books_genres", genres, postgresql_using="gin"),
        Index("ix_books_author", "author"),
        Index("ix_books_language", "language"),
    )

