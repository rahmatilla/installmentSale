from fastapi import APIRouter, HTTPException
from schemas import Sale
from crud.sale import create_sale, get_sale, get_sales, update_sale, delete_sale
from typing import List

router = APIRouter(
    prefix='/sale',
    tags=['sale']
)

@router.post("/sales/", response_model=Sale)
async def create_sale_api(sale: Sale):
    return await create_sale(sale)

@router.get("/sales/")
async def get_sales_api(skip: int = 0, limit: int = 10):
    return await get_sales(skip, limit)

@router.get("/sales/{sale_id}", response_model=Sale)
async def get_sale_api(sale_id: int):
    sale = await get_sale(sale_id)
    if sale:
        return sale
    else:
        raise HTTPException(status_code=404, detail="Sale not found")

@router.put("/sales/{sale_id}", response_model=Sale)
async def update_sale_api(sale_id: int, sale: Sale):
    return await update_sale(sale_id, sale)

@router.delete("/sales/{sale_id}", response_model=Sale)
async def delete_sale_api(sale_id: int):
    return await delete_sale(sale_id)