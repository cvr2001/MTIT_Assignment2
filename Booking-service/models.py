from pydantic import BaseModel
from typing import Optional

class Booking(BaseModel):
    id: int
    movie: str
    theater: str
    seats: int

class BookingCreate(BaseModel):
    movie: str
    theater: str
    seats: int

class BookingUpdate(BaseModel):
    movie: Optional[str] = None
    theater: Optional[str] = None
    seats: Optional[int] = None