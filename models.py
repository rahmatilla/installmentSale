from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import datetime



Base = declarative_base()

class Customer(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String, unique=True, nullable=False)
    role = Column(String)
    password = Column(String, nullable=False)

    # Establish a one-to-many relationship from User to Sale
    sales = relationship("Sale", back_populates="user")

class TokenTable(Base):
    __tablename__ = "token"
    user_id = Column(Integer)
    access_toke = Column(String(450), primary_key=True)
    refresh_toke = Column(String(450),nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.datetime.now)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    price = Column(Float)

 # Establish a one-to-many relationship from Product to Sale
    sales = relationship("Sale", back_populates="product")

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    total_amount = Column(Float)
    down_payment = Column(Float)
    remaining_amount = Column(Float)
    sale_date = Column(Date, default=func.now())

    # Establishing relationships to User and Product
    user = relationship("User", back_populates="sales")
    product = relationship("Product", back_populates="sales")

    # Establish a one-to-many relationship from Sale to Installment
    installments = relationship("Installment", back_populates="sale")

class Installment(Base):
    __tablename__ = "installments"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey('sales.id'))
    installment_number = Column(Integer)
    due_date = Column(Date)
    amount = Column(Float)
    payment_date = Column(Date, nullable=True)

    # Establishing a relationship to Sale
    sale = relationship("Sale", back_populates="installments")
