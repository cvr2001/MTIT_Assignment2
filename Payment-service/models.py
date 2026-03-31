from pydantic import BaseModel
from typing import Optional

class Payment(BaseModel):
    id: int
    booking_id: int
    amount: float
    payment_method: str
    status: str

class PaymentCreate(BaseModel):
    booking_id: int
    amount: float
    payment_method: str
    status: str

class PaymentUpdate(BaseModel):
    booking_id: Optional[int] = None
    amount: Optional[float] = None
    payment_method: Optional[str] = None
    status: Optional[str] = None