from decimal import Decimal
from datetime import datetime, timezone
from uuid import uuid4
from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Numeric, Index, UniqueConstraint, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship 
from .database import Base

class UserRole(PyEnum):
    USER = "user"
    ADMIN = "admin"

class CustomerType(PyEnum):
    LEGAL_ENTITY = "legal_entity"
    INDIVIDUAL = "individual"

class User(Base): 
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True) 
    surname = Column(String(100), nullable=False) 
    name = Column(String(100), nullable=False)
    patronymic = Column(String(100), nullable=True)
    phone_number = Column(String(20), nullable=False, unique=True, index=True)
    inn = Column(String(12), nullable=False, unique=True, index=True)
    role = Column(Enum(UserRole, native_enum=False, length=50), nullable=False, default=UserRole.USER)
    
    products = relationship("Product", back_populates="user", cascade="all, delete-orphan")
    customers = relationship("Customer", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, phone={self.phone_number}, role={self.role.value})>"

class Product(Base): 
    __tablename__ = "products"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True) 
    name = Column(String(200), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    is_countable = Column(Boolean, nullable=False, default=True)  # True - исчисляемый, False - неисчисляемый
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    user = relationship("User", back_populates="products")
    orderproducts = relationship("OrderProduct", back_populates="product")
    
    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price})>"

class Customer(Base): 
    __tablename__ = "customers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True) 
    name = Column(String(200), nullable=False)
    inn = Column(String(12), nullable=False, index=True)
    customer_type = Column(Enum(CustomerType, native_enum=False, length=50), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
   
    user = relationship("User", back_populates="customers")
    orders = relationship("Order", back_populates="customer")
    
    __table_args__ = (
        UniqueConstraint('inn', 'user_id', name='uq_customer_inn_user'),
    )
    
    def __repr__(self):
        return f"<Customer(id={self.id}, name={self.name}, inn={self.inn}, type={self.customer_type.value})>"

class Order(Base): 
    __tablename__ = "orders"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True) 
    number = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
  
    user = relationship("User", back_populates="orders")
    customer = relationship("Customer", back_populates="orders")
    orderproducts = relationship("OrderProduct", back_populates="order", cascade="all, delete-orphan")
    
    __table_args__ = (
        UniqueConstraint('number', 'user_id', name='uq_order_number_user'),
    )
    
    def __repr__(self):
        return f"<Order(id={self.id}, number={self.number}, created_at={self.created_at})>"

class OrderProduct(Base): 
    __tablename__ = "order_products"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id", ondelete="RESTRICT"), nullable=False, index=True)
    product = relationship("Product", back_populates="orderproducts")
    order = relationship("Order", back_populates="orderproducts")
    
    def __repr__(self):
        return f"<OrderProduct(id={self.id}, quantity={self.quantity}, price={self.price})>"

class OneTimePassword(Base): 
    __tablename__ = "one_time_passwords"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True) 
    phone_number = Column(String(20), nullable=False, index=True)
    code = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    is_used = Column(Boolean, nullable=False, default=False)
    
    def __repr__(self):
        return f"<OneTimePassword(id={self.id}, phone={self.phone_number}, is_used={self.is_used})>"
