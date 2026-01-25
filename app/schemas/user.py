from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str

    model_config = ConfigDict(extra="forbid")


class UserLogin(UserBase):
    password: str

    model_config = ConfigDict(extra="forbid")


class UserResponse(UserBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="forbid")
