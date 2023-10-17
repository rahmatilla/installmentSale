from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class Customer(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: str

class Product(BaseModel):
    product_name: str
    price: float

class Sale(BaseModel):
    customer_id: int
    product_id: int
    total_amount: float
    down_payment: float
    remaining_amount: float

class Installment(BaseModel):
    sale_id: int
    installment_number: int
    due_date: date
    amount: float
    payment_date: Optional[date] = None