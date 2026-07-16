from typing import TypedDict, Annotated
import operator
import uuid

class ParsedIntent(TypedDict):
    """Output of QueryParserAgent -- LLM extract from raw query"""
    genres: list[str]
    mood: str | None
    pages_min: int | None
    pages_max: int | None
    language: str | None
    raw_query: str

class BookResult(TypedDict):
    """1 cuốn sách trong kết quả search."""
    id: str
    title: str
    author: str
    genres: list[str]
    pages: int | None
    avg_rating: float | None
    score: float          # relevance score từ vector search
    reason: str | None    # lý do gợi ý — sinh bởi reranker
 
class SearchState(TypedDict):
    """
    State cho search graph.
    Mỗi node nhận SearchState vào, trả về dict update một phần.
    """
    # Input từ user
    query: str
    user_id: str | None       # None nếu guest
 
    # Sau QueryParserAgent
    parsed_intent: ParsedIntent | None
 
    # Sau HybridSearch + MetadataFilter
    candidate_books: list[BookResult]
 
    # Sau RerankerAgent
    final_results: list[BookResult]
 
    # Session ID để log vào DB
    session_id: str | None
 
    # Nếu có lỗi ở bước nào
    error: str | None

# ── Research State ─────────────────────────────────────────────
# Dùng cho flow: user hỏi về 1 cuốn sách cụ thể
 
class Message(TypedDict):
    role: str      # "user" hoặc "assistant"
    content: str
 
 
class ResearchState(TypedDict):
    """
    State cho research Q&A graph.
    """
    # Input
    book_id: str
    user_id: str
    question: str
 
    # Context từ DB
    book_title: str | None
    reviews: list[str]        # list raw review content
 
    # Conversation history
    messages: Annotated[list[Message], operator.add]  # operator.add = append thay vì replace
 
    # Output
    answer: str | None
    error: str | None

# ── Helper functions ───────────────────────────────────────────
 
def create_search_state(query: str, user_id: str | None = None) -> SearchState:
    """Tạo SearchState mới với giá trị mặc định."""
    return SearchState(
        query=query,
        user_id=user_id,
        parsed_intent=None,
        candidate_books=[],
        final_results=[],
        session_id=str(uuid.uuid4()),
        error=None,
    )
 
 
def create_research_state(
    book_id: str,
    user_id: str,
    question: str,
    history: list[Message] | None = None,
) -> ResearchState:
    """Tạo ResearchState mới."""
    return ResearchState(
        book_id=book_id,
        user_id=user_id,
        question=question,
        book_title=None,
        reviews=[],
        messages=history or [],
        answer=None,
        error=None,
    )