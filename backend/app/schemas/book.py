import uuid
from pydantic import BaseModel


class BookOut(BaseModel):
    """Dùng trong search results — chỉ expose những gì frontend cần."""
    id: uuid.UUID
    title: str
    author: str
    genres: list[str]
    pages: int | None
    year: int | None
    language: str
    cover_url: str | None
    avg_rating: float | None
    review_count: int

    model_config = {"from_attributes": True}


class BookDetail(BookOut):
    """Dùng trong book detail page — thêm external links."""
    isbn: str | None
    publisher: str | None
    tiki_url: str | None
    fahasa_url: str | None
    goodreads_url: str | None


class BookSearchResult(BaseModel):
    """Một item trong search response — kèm match score và lý do gợi ý."""
    book: BookOut
    score: float
    reason: str | None = None   