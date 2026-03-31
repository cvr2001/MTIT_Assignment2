from pydantic import BaseModel
from typing import Optional

class Theater(BaseModel):
    id: int
    name: str
    capacity: int
    screen_type: str

class TheaterCreate(BaseModel):
    name: str
    capacity: int
    screen_type: str

class TheaterUpdate(BaseModel):
    name: Optional[str] = None
    capacity: Optional[int] = None
    screen_type: Optional[str] = None