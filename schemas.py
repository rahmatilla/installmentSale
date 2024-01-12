from pydantic import BaseModel
from typing import List, Optional
from datetime import date
import datetime

class User(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    role: str
    password: str

class requestdetails(BaseModel):
    phone_number:str
    password:str
        
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

class changepassword(BaseModel):
    phone_number:str
    old_password:str
    new_password:str

class TokenCreate(BaseModel):
    user_id:str
    access_token:str
    refresh_token:str
    status:bool
    created_date:datetime.datetime

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