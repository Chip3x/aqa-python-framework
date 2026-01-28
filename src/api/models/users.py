from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user model with common fields."""

    email: EmailStr
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)


class UserCreate(UserBase):
    """User creation request model."""

    password: str = Field(min_length=8)


class UserUpdate(BaseModel):
    """User update request model."""

    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None


class UserResponse(UserBase):
    """User response model."""

    id: int
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None


class UserListResponse(BaseModel):
    """User list response model."""

    items: list[UserResponse]
    total: int
    page: int
    per_page: int
