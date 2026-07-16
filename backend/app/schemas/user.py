import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: uuid.UUID
    email: str
    name: str
    avatar_url: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class UserProfile(BaseModel):
    id: uuid.UUID
    email: str
    name: str
    avatar_url: str | None
    profile_vector: dict
    psych_scores: dict
    created_at: datetime

    model_config = {"from_attributes": True}

    
class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"