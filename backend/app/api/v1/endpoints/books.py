from turtle import title
import uuid
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.schemas.book import BookCreate, BookOut
from app.models.book import Book


router = APIRouter()


@router.get("/books", response_model=list[BookOut])
async def get_all_books(
    author: str | None = None, 
    max_pages: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    # select(Book) == "SELECT * FROM books"
    query = select(Book) 

    if author:
        query = query.where(Book.author.ilike(f"%{author}%")) # ilike both lower and upper 
    if max_pages:
        query = query.where(Book.pages <= max_pages)

    result = await db.scalars(query)
    return result.all()

@router.get("/books/{book_id}", response_model=BookOut)
async def get_book(book_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    book = await db.scalar(select(Book).where(Book.id == book_id))
    
    if not book:
        raise HTTPException(status_code=400, detail=f"Not found book {book_id}")
    return book

@router.post("/books", response_model=BookOut, status_code=201)
async def create_book(body: BookCreate, db: AsyncSession = Depends(get_db)):
    book = Book(
        title = body.title,
        author = body.author,
        pages = body.pages,
    )
    db.add(book)
    await db.flush() # Storage into db but not commit yet

    return book

@router.put("/books/{book_id}", response_model=BookOut)
async def update_book(book_id: uuid.UUID, body: BookCreate, db: AsyncSession = Depends(get_db)):
    book = await db.scalar(select(book).where(Book.id == book_id))
    if not book:    
        raise HTTPException(status_code=404, detail=f"Not found {book_id}")

    book.title = body.title
    book.author = body.author
    book.pages = body.pages

    await db.flush()
    return book

@router.delete("/books/{book_id}")
async def delete_book(book_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    book = await db.scalar(select(Book).where(Book.id == book_id))

    if not book:
       raise HTTPException(status_code=404, detail=f"Not found book {book_id}")            
    
    await db.delete(book)
    return {"message": f"Đã xóa sách {book_id}"}