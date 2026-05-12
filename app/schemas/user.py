from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserOut(BaseModel):
    id: UUID  # ← was int, change to UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    tier: str = "free"
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True
