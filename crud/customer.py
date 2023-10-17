from sqlalchemy.ext.asyncio import AsyncSession
from schemas import Customer
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from database import AsyncSessionLocal

async def create_customer(customer: Customer):
    async with AsyncSessionLocal() as session:
        try:
            db_customer = Customer(**customer.dict())
            session.add(db_customer)
            await session.commit()
            await session.refresh(db_customer)
            return db_customer
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Customer already exists")

async def get_customers(skip: int = 0, limit: int = 10):
    async with AsyncSession() as session:
        query = session.query(Customer).offset(skip).limit(limit)
        return await query.gino.all()

async def get_customer(customer_id: int):
    async with AsyncSession() as session:
        return await session.get(Customer, customer_id)

async def update_customer(customer_id: int, customer: Customer):
    async with AsyncSession() as session:
        db_customer = await session.get(Customer, customer_id)
        if db_customer:
            for key, value in customer.dict(exclude_unset=True).items():
                setattr(db_customer, key, value)
            await session.commit()
            await session.refresh(db_customer)
            return db_customer
        else:
            raise HTTPException(status_code=404, detail="Customer not found")

async def delete_customer(customer_id: int):
    async with AsyncSession() as session:
        db_customer = await session.get(Customer, customer_id)
        if db_customer:
            session.delete(db_customer)
            await session.commit()
            return db_customer
        else:
            raise HTTPException(status_code=404, detail="Customer not found")