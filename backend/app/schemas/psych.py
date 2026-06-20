import uuid
from datetime import datetime
from typing import Literal
from pydantic import BaseModel


class TestSubmit(BaseModel):
    test_level: Literal["quick", "standard", "deep"]
    answers: dict  # { question_id: answer_value }


class Big5Scores(BaseModel):
    openness: float
    conscientiousness: float
    extraversion: float
    agreeableness: float
    neuroticism: float


class TestScores(BaseModel):
    big5: Big5Scores | None = None
    mbti: str | None = None          # "INFP", "ENTJ", ...
    reading_style: str | None = None # "emotional", "analytical", ...


class TestResult(BaseModel):
    id: uuid.UUID
    test_level: str
    scores: TestScores
    taken_at: datetime

    model_config = {"from_attributes": True}