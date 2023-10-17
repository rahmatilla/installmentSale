from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    email = Column(String)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    price = Column(Float)

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    total_amount = Column(Float)
    down_payment = Column(Float)
    remaining_amount = Column(Float)
    sale_date = Column(Date, default=func.now())

    # Establishing relationships to Customer and Product
    customer = relationship("Customer", back_populates="sales")
    product = relationship("Product", back_populates="sales")

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
