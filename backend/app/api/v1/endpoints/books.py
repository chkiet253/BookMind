import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.book import Book
from app.models.review import Review
from app.schemas.book import BookDetail, BookOut

router = APIRouter(prefix="/books", tags=["books"])

