from sqlmodel import Field,SQLModel, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from decimal import Decimal
from sqlalchemy import DateTime, func, Column, Integer
from typing import Optional

class Supplier(SQLModel, table=True):
    __tablename__ = 'supplier'
    __table_args__ = {'extend_existing': True}
    id: int = Field(default=None, nullable=False, primary_key=True)
    name: str = Field(default=None, nullable=False, unique=True)
    contact_info: str = Field()
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime(), onupdate=func.now(), nullable=True))

    class Config:
        arbitrary_types_allowed = True

class Product(SQLModel, table=True):
    __tablename__ = 'product'
    __table_args__ = {'extend_existing': True}
    id: int = Field(default=None, nullable=False, primary_key=True)
    name: str = Field(default=None, nullable=False, unique=True)
    description: str = Field()
    price: Decimal = Field()
    supplier_id: int= Field(default=None, foreign_key="supplier.id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime(), onupdate=func.now()))

class Customer(SQLModel, table=True):
    __tablename__ = 'customer'
    __table_args__ = {'extend_existing': True}
    id: int = Field(default=None, nullable=False, primary_key=True)
    name: str = Field(default=None, nullable=False)
    contact_info: str = Field()
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime(), onupdate=func.now()))

class OrderStatus(SQLModel, table=True):
    __tablename__ = "order_status"
    __table_args__ = {'extend_existing': True}
    id: int = Field(default=None, nullable=False, primary_key=True)
    name: str = Field(default=None, nullable=False, unique=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime(), onupdate=func.now()))

class Orders(SQLModel, table=True):
    __tablename__ = 'orders'
    __table_args__ = {'extend_existing': True}
    id: int = Field(default=None, nullable=False, primary_key=True)
    customers_id:int = Field(default=None, foreign_key="customer.id")
    order_status_id:int = Field(default=None, foreign_key="order_status.id")
    order_date: datetime = Field(nullable=False)
    contact_info: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime(), onupdate=func.now()))

class OrdersItems(SQLModel, table=True):
    __tablename__ = "order_items"
    __table_args__ = {'extend_existing': True}
    id: int = Field(default=None, nullable=False, primary_key=True)
    order_id:int = Field(default=None, foreign_key="orders.id")
    product_id:int = Field(default=None, foreign_key="product.id")
    quantity:int = Field(nullable=False)
    price: Decimal = Field()
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime(), onupdate=func.now()))

class ShipmentStatus(SQLModel, table=True):
    __tablename__ = "shipment_status"
    __table_args__ = {'extend_existing': True}
    id: int = Field(default=None, nullable=False, primary_key=True)
    name: str = Field(default=None, nullable=False, unique=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime(), onupdate=func.now()))

class Shipment(SQLModel, table=True):
    __tablename__ = "shipment"
    __table_args__ = {'extend_existing': True}
    id: int = Field(default=None, nullable=False, primary_key=True)
    order_id:int = Field(default=None, foreign_key="orders.id")
    shipment_date: datetime = Field()
    delivery_date: datetime = Field()
    shipment_status_id:int = Field(default=None, foreign_key="shipment_status.id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime(), onupdate=func.now()))


