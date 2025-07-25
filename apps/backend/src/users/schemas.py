from uuid import UUID
from pydantic import BaseModel , ConfigDict, EmailStr, Field
from datetime import datetime


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: EmailStr
    role: str
    created_at: datetime

class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=50)
    email: EmailStr
    direction: str

