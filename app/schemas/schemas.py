from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class BookCreate(BaseModel):
    """Schema for creating a new book"""
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    genre: Optional[str]
    year_published: Optional[int]
    summary: Optional[str]


class BookOut(BookCreate):
    """Schema for outputting book details"""
    id: int

    class Config:
        from_attributes = True


class ReviewCreate(BaseModel):
    """Schema for creating a new review"""
    review_text: str = Field(...)
    rating: int = Field(..., ge=1, le=5)


class ReviewOut(ReviewCreate):
    """Schema for outputting review details"""
    id: int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    """Schema for creating a new user"""
    username: str = Field(...)
    email: EmailStr
    password: str
    role: Optional[str] = "user"


class UserOut(BaseModel):
    """Schema for outputting user details"""
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for JWT token"""
    access_token: str
    token_type: str = "bearer"
