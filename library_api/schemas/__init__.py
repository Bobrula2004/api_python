from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# Схемы
class AuthorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    bio: Optional[str] = None


class Author(AuthorBase):
    id: int
    
    class Config:
        from_attributes = True



class GenreBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class GenreCreate(GenreBase):
    pass


class GenreUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)


class Genre(GenreBase):
    id: int
    
    class Config:
        from_attributes = True



class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=300)
    isbn: Optional[str] = Field(None, max_length=20)
    publication_year: Optional[int] = Field(None, ge=1000, le=2100)
    description: Optional[str] = None
    page_count: Optional[int] = Field(None, ge=1)
    author_id: int
    genre_id: int


class BookCreate(BookBase):
    title: str = Field(..., min_length=1, max_length=300)
    author_id: int
    genre_id: int


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=300)
    isbn: Optional[str] = Field(None, max_length=20)
    publication_year: Optional[int] = Field(None, ge=1000, le=2100)
    description: Optional[str] = None
    page_count: Optional[int] = Field(None, ge=1)
    author_id: Optional[int] = None
    genre_id: Optional[int] = None


class Book(BookBase):
    id: int
    created_at: datetime

    author: Optional[Author] = None
    genre: Optional[Genre] = None
    
    class Config:
        from_attributes = True



class PaginatedResponse(BaseModel):
    items: list[Book]
    total: int
    page: int
    limit: int
    pages: int