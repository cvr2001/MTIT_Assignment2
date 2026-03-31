from pydantic import BaseModel
from typing import Optional

class Movie(BaseModel):
    id: int
    title: str
    director: str
    genre: str
    duration_minutes: int
    language: str

class MovieCreate(BaseModel):
    title: str
    director: str
    genre: str
    duration_minutes: int
    language: str

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    director: Optional[str] = None
    genre: Optional[str] = None
    duration_minutes: Optional[int] = None
    language: Optional[str] = None