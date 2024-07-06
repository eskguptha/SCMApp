from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlmodel import SQLModel


class SupplierCreateUpdate(SQLModel):
    name: str
    contact_info: str

class ProductCreateUpdate(SQLModel):
    name: str
    description: str
    price:Decimal
    supplier_id:int

class CustomerCreateUpdate(SQLModel):
    name: str
    contact_info: str

class OrderStatusCreateUpdate(SQLModel):
    name: str    

class OrderCreateUpdate(SQLModel):
    customers_id: str
    order_status_id:int
    order_date:datetime
    contact_info:str
    order_items:list