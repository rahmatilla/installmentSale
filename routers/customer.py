from fastapi import APIRouter, HTTPException
from schemas import Customer
from crud.customer import create_customer, get_customer, get_customers, update_customer, delete_customer
from typing import List

router = APIRouter(
    prefix='/customer',
    tags=['customer']
)

@router.post("/customers/", response_model=Customer)
async def create_customer_api(customer: Customer):
    return await create_customer(customer)

@router.get("/customers/", response_model=List[Customer])
async def get_customers_api(skip: int = 0, limit: int = 10):
    return await get_customers(skip, limit)

@router.get("/customers/{customer_id}", response_model=Customer)
async def get_customer_api(customer_id: int):
    customer = await get_customer(customer_id)
    if customer:
        return customer
    else:
        raise HTTPException(status_code=404, detail="Customer not found")

@router.put("/customers/{customer_id}", response_model=Customer)
async def update_customer_api(customer_id: int, customer: Customer):
    return await update_customer(customer_id, customer)

@router.delete("/customers/{customer_id}", response_model=Customer)
async def delete_customer_api(customer_id: int):
    return await delete_customer(customer_id)