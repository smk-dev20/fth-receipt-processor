from pydantic import BaseModel
from typing import List
from datetime import date, time

class ReceiptItemBase(BaseModel):
    shortDescription: str
    price: float

class ReceiptBase(BaseModel):
    retailer: str
    purchaseDate: date
    purchaseTime: time
    items: List[ReceiptItemBase]
    total: float


