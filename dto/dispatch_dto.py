from typing import Optional
from pydantic import BaseModel
from datetime import date


class RecipientSchema(BaseModel):
    full_name: Optional[str] = None
    address: Optional[str] = None
    phone_number_1: Optional[str] = None
    phone_number_2: Optional[str] = None

class DispatchSchema(BaseModel):
    recipient_id: Optional[str] = None  
    content: Optional[str] = None
    weight: Optional[int] = None
    note: Optional[str] = None
    delievery_date: Optional[date] = None
    code: Optional[str] = None
    new_recipient: Optional[RecipientSchema] = None

