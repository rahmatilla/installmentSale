from fastapi import APIRouter, HTTPException, Depends
from schemas import User, TokenSchema, requestdetails, changepassword
from crud.user import create_user, get_user, get_users, update_user, delete_user, login, change_password, logout
from typing import List
from auth_bearer import JWTBearer

router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.post("/users/", response_model=User)
async def create_user_api(user: User):
    return await create_user(user)

@router.post("/login/", response_model=TokenSchema)
async def login_api(request: requestdetails):
    return await login(request)

@router.post("/change-password")
async def change_password_api(request:changepassword):
    return change_password(request)

@router.post("/logout", dependencies=Depends(JWTBearer()))
async def logout_api():
    return logout(dependencies)

@router.get("/users/", dependencies=Depends(JWTBearer()))
async def get_users_api(skip: int = 0, limit: int = 10):
    return await get_users(skip, limit)

@router.get("/users/{user_id}", response_model=User)
async def get_user_api(user_id: int):
    return await get_user(user_id)
    

@router.put("/users/{user_id}", response_model=User)
async def update_user_api(user_id: int, user: User):
    return await update_user(user_id, user)

@router.delete("/users/{user_id}", response_model=User)
async def delete_user_api(user_id: int):
    return await delete_user(user_id)