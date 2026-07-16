import uuid
from pydantic import BaseModel, Field
from app.schemas.book import BookSearchResult


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    limit: int = Field(default=5, ge=1, le=20)


class ParsedIntent(BaseModel):
    """Output của QueryParserAgent — dùng nội bộ giữa agents."""
    genres: list[str] = []
    mood: str | None = None
    pages_min: int | None = None
    pages_max: int | None = None
    language: str | None = None
    raw_query: str = ""


class SearchResponse(BaseModel):
    results: list[BookSearchResult]
    session_id: uuid.UUID
    parsed_intent: ParsedIntent