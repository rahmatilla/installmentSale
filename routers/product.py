from fastapi import APIRouter, HTTPException
from schemas import Product
from crud.product import create_product, get_product, get_products, update_product, delete_product
from typing import List

router = APIRouter(
    prefix='/product',
    tags=['product']
)

@router.post("/products/", response_model=Product)
async def create_product_api(product: Product):
    return await create_product(product)

@router.get("/products/")
async def get_products_api(skip: int = 0, limit: int = 10):
    return await get_products(skip, limit)

@router.get("/products/{product_id}", response_model=Product)
async def get_product_api(product_id: int):
    product = await get_product(product_id)
    if product:
        return product
    else:
        raise HTTPException(status_code=404, detail="Product not found")

@router.put("/products/{product_id}", response_model=Product)
async def update_product_api(product_id: int, product: Product):
    return await update_product(product_id, product)

@router.delete("/customers/{product_id}", response_model=Product)
async def delete_product_api(product_id: int):
    return await delete_product(product_id)