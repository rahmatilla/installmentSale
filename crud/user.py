from schemas import User, requestdetails, changepassword
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from database import AsyncSessionLocal
import models
from sqlalchemy.future import select
from utils import get_hashed_password, verify_password, create_access_token, create_refresh_token, JWT_SECRET_KEY, ALGORITHM
import jwt
from datetime import datetime

async def create_user(user: User):
    async with AsyncSessionLocal() as session:
        query = select(models.User).where(models.User.phone_number == user.phone_number)
        result = await session.execute(query)
        if result:
            raise HTTPException(status_code=400, detail="Phone number already registered")
        
        encrypted_password = get_hashed_password(user.password)
        new_user = models.User(first_name=user.first_name, last_name=user.last_name, password=encrypted_password )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return {"message":"user created successfully"}

        # try:
        #     db_user = models.User(**user.dict())
        #     session.add(db_user)
        #     await session.commit()
        #     await session.refresh(db_user)
        #     return db_user
        # except IntegrityError:
        #     raise HTTPException(status_code=400, detail="User already exists")

async def login(request: requestdetails):
    async with AsyncSessionLocal() as session:
        user = select(models.User).where(models.User.phone_number == request.phone_number)

        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
        hashed_pass = user.password
        if not verify_password(request.password, hashed_pass):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Incorrect password")
    
        access=create_access_token(user.id)
        refresh = create_refresh_token(user.id)

        token_db = models.TokenTable(user_id=user.id,  access_toke=access,  refresh_toke=refresh, status=True)
        session.add(token_db)
        session.commit()
        session.refresh(token_db)
        return {
            "access_token": access,
            "refresh_token": refresh,
        }

async def change_password(request:changepassword):
    async with AsyncSessionLocal() as session:
        user = select(models.User).where(models.User.phone_number == request.phone_number)
        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    
        if not verify_password(request.old_password, user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password")
    
        encrypted_password = get_hashed_password(request.new_password)
        user.password = encrypted_password
        session.commit()
        return {"message": "Password changed successfully"}
    
async def logout(token):
    async with AsyncSessionLocal() as session:
        payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
        user_id = payload['sub']
        token_record = session.query(models.TokenTable).all()
        info=[]
        for record in token_record :
            print("record",record)
            if (datetime.utcnow() - record.created_date).days >1:
                info.append(record.user_id)
        if info:
            existing_token = session.query(models.TokenTable).where(models.TokenTable.user_id.in_(info)).delete()
            session.commit()
        
        existing_token = session.query(models.TokenTable).filter(models.TokenTable.user_id == user_id, models.TokenTable.access_toke==token).first()
        if existing_token:
            existing_token.status=False
            session.add(existing_token)
            session.commit()
            session.refresh(existing_token)
        return {"message":"Logout Successfully"} 

    
async def get_users(skip: int = 0, limit: int = 10):
    async with AsyncSessionLocal() as session:
        query = select(models.User).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

async def get_user(user_id: int):
    async with AsyncSessionLocal() as session:
        db_user = await session.get(models.User, user_id)
        if db_user:
            return db_user
        else:
            raise HTTPException(status_code=404, detail="User not found")

async def update_user(user_id: int, user: User):
    async with AsyncSessionLocal() as session:
        db_user = await session.get(models.User, user_id)
        if db_user:
            for key, value in user.dict(exclude_unset=True).items():
                setattr(db_user, key, value)
            await session.commit()
            await session.refresh(db_user)
            return db_user
        else:
            raise HTTPException(status_code=404, detail="User not found")

async def delete_user(user_id: int):
    async with AsyncSessionLocal() as session:
        db_user = await session.get(models.User, user_id)
        if db_user:
            await session.delete(db_user)
            await session.commit()
            return db_user
        else:
            raise HTTPException(status_code=404, detail="User not found")