from pydantic import BaseModel
from typing import Optional

class Show(BaseModel):
    id: int
    movie_id: int
    theater_id: int
    start_time: str

class ShowCreate(BaseModel):
    movie_id: int
    theater_id: int
    start_time: str

class ShowUpdate(BaseModel):
    movie_id: Optional[int] = None
    theater_id: Optional[int] = None
    start_time: Optional[str] = None