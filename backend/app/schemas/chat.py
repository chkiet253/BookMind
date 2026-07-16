import uuid
from datetime import datetime
from typing import Literal
from pydantic import BaseModel


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    timestamp: datetime


class ChatRequest(BaseModel):
    book_id: uuid.UUID
    message: str


class ChatResponse(BaseModel):
    chat_id: uuid.UUID
    answer: str
    messages: list[Message]