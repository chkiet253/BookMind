from fastapi import APIRouter, HTTPException
from app.schemas.book import BookCreate

router = APIRouter()

fake_books = [
    {"id": 1, "title": "Nhà giả kim", "author": "Paulo Coelho", "pages": 224},
    {"id": 2, "title": "Đắc nhân tâm", "author": "Dale Carnegie", "pages": 320},
    {"id": 3, "title": "Sapiens", "author": "Yuval Noah Harari", "pages": 559},
]

@router.get("/books")
def get_all_books():
    return fake_books

@router.get("/books/{book_id}")
def get_book(book_id: int):
    for book in fake_books:
        if book["id"] == book_id:
            return book

    raise HTTPException(status_code=400, detail=f"Not found book {book_id}")

@router.post("/books")
def create_book(book: BookCreate):
    new_id = len(fake_books) + 1
    new_book = {
        "id": new_id,
        "title": book.title,
        "author": book.author,
        "pages": book.pages,
    }
    fake_books.append(new_book) 

    return new_book

@router.put("/books/{book_id}")
def update_book(book_id: int, book: BookCreate):
    