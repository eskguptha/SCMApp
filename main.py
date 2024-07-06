from fastapi import Depends, FastAPI, Response
from pydantic import BaseModel
from sqlmodel import select
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from models import Product, Supplier, Customer, OrderStatus,Orders
from schemas import SupplierCreateUpdate, ProductCreateUpdate, OrderStatusCreateUpdate, CustomerCreateUpdate, OrderCreateUpdate
from db import get_session, init_db
import uvicorn
from typing import List, Dict


app = FastAPI( title='SCM API',description='Supply Chain Management System', swagger_ui_parameters={"syntaxHighlight.theme": "obsidian", "deepLinking": False})

@app.on_event("startup")
async def on_startup():
    await init_db()

class ResponseModel(BaseModel):
    status: str = None
    data: Dict = {}
    message: str = None

@app.get("/ping,", tags=["health Check"])
async def pong():
    return {"ping": "pong!"}

@app.get("/suppliers", tags=["List Suppliers"], response_model=ResponseModel)
async def list_suppliers(session: AsyncSession = Depends(get_session)):
    try:
        queryset_result = await session.execute(select(Supplier))
        result = [each.json() for each in queryset_result.scalars().all()]
        response_data = ResponseModel(status= "OK", data={"result" : result}, message=f"Records Total: {len(result)}")
        status_code = 200
    except Exception as e:
        status_code = 500
        response_data = ResponseModel(status= "NotOK", data= {"error" :  str(e)}, message="Something went wrong")
    return JSONResponse(status_code=status_code, content=response_data.dict())

@app.get("/suppliers/{id}", tags=["get Supplier details"], response_model=ResponseModel)
async def get_supplier(id:int,session: AsyncSession = Depends(get_session)):
    try:
        statement = select(Supplier).where(Supplier.id == id)
        result = (await session.exec(statement)).first()
        if result:
            response_data = ResponseModel(status= "OK", data={"result" : result.json()}, message="1 Record found")
            status_code = 200
        else:
            response_data = ResponseModel(status= "NotOK", data= {"error" : "invalid Record Id"}, message=f"No Records found")
            status_code = 400
    except Exception as e:
        response_data = ResponseModel(status= "NotOK", data= {"error" :  str(e)}, message="Something went wrong")
        status_code = 500
    return JSONResponse(status_code=status_code, content=response_data.dict())

@app.post("/suppliers", tags=["create new Supplier"], response_model=ResponseModel)
async def create_supplier(SupplierCreateUpdate: SupplierCreateUpdate, session: AsyncSession = Depends(get_session)):
    try:
        statement = select(Supplier).where(Supplier.name == SupplierCreateUpdate.name)
        results = await session.exec(statement)
        if len(results.all()) > 0:
            response_data = ResponseModel(status= "NotOK", data={"error" :  SupplierCreateUpdate.name}, message=f"Record already exists with name field value as '{suppliderCreate.name}'")
            status_code = 400
        else:
            supplier_cls = Supplier(name=SupplierCreateUpdate.name, contact_info=SupplierCreateUpdate.contact_info)
            session.add(supplier_cls)
            await session.commit()
            await session.refresh(supplier_cls)
            response_data = ResponseModel(status= "OK", data={"id" : supplier_cls.id}, message="Record Created Successfully")
            status_code = 201
    except Exception as e:
        status_code = 500
        response_data = ResponseModel(status= "NotOK", data= {"error" :  str(e)}, message="Something went wrong")
    return JSONResponse(status_code=status_code, content=response_data.dict())

@app.put("/suppliers/{id}", tags=["Update supplier details"])
async def update_supplier(id: int, supplierUpdate: SupplierCreateUpdate, session: AsyncSession = Depends(get_session)):
    try:
        queryset_result = await session.get(Supplier, id)
        if queryset_result:
            queryset_result.name=supplierUpdate.name
            queryset_result.contact_info=supplierUpdate.contact_info
            session.add(queryset_result)
            await session.commit()
            await session.refresh(queryset_result)
            response_data = ResponseModel(status= "OK", data={"id" : queryset_result.id}, message="Record updated Successfully")
            status_code = 200
        else:
            response_data = ResponseModel(status= "NotOK", data={"error" : "invalid Record id"}, message="Record Not Exist")
            status_code = 400
    except Exception as e:
        status_code = 500
        response_data = ResponseModel(status= "NotOK", data= {"error" :  str(e)}, message="Something went wrong")
    return JSONResponse(status_code=status_code, content=response_data.dict())

@app.get("/products", tags=["List Products"], response_model=ResponseModel)
async def list_products(session: AsyncSession = Depends(get_session)):
    try:
        queryset_result = await session.execute(select(Product))
        result = [each.json() for each in queryset_result.scalars().all()]
        response_data = ResponseModel(status= "OK", data={"result" : result}, message=f"Records Total: {len(result)}")
        status_code = 200
    except Exception as e:
        status_code = 500
        response_data = ResponseModel(status= "NotOK", data= {"error" :  str(e)}, message="Something went wrong")
    return JSONResponse(status_code=status_code, content=response_data.dict())

@app.get("/products/{suplier_id}", tags=["get Product details"], response_model=ResponseModel)
async def get_product(id:int,session: AsyncSession = Depends(get_session)):
    try:
        statement = select({Product}).where(Product.id == id)
        result = (await session.exec(statement)).first()
        if result:
            response_data = ResponseModel(status= "OK", data={"result" : result.json()}, message="1 Record found")
            status_code = 200
        else:
            response_data = ResponseModel(status= "NotOK", data= {"error" : "invalid Record Id"}, message=f"No Records found")
            status_code = 400
    except Exception as e:
        response_data = ResponseModel(status= "NotOK", data= {"error" :  str(e)}, message="Something went wrong")
        status_code = 500
    return JSONResponse(status_code=status_code, content=response_data.dict())

@app.post("/products", tags=["create new Product"], response_model=ResponseModel)
async def create_product(ProductCreateUpdate: ProductCreateUpdate, session: AsyncSession = Depends(get_session)):
    try:
        statement = select(Product).where(Product.name == ProductCreateUpdate.name)
        results = await session.exec(statement)
        if len(results.all()) > 0:
            response_data = ResponseModel(status= "NotOK", data={"error" :  ProductCreateUpdate.name}, message=f"Record already exists with name field value as '{ProductCreateUpdate.name}'")
            status_code = 400
        else:
            product_cls = Product(name=ProductCreateUpdate.name, description=ProductCreateUpdate.description, price=ProductCreateUpdate.price,  supplier_id=ProductCreateUpdate.supplier_id)
            session.add(product_cls)
            await session.commit()
            await session.refresh(product_cls)
            response_data = ResponseModel(status= "OK", data={"id" : product_cls.id}, message="Record Created Successfully")
            status_code = 201
    except Exception as e:
        status_code = 500
        response_data = ResponseModel(status= "NotOK", data= {"error" :  str(e)}, message="Something went wrong")
    return JSONResponse(status_code=status_code, content=response_data.dict())

@app.put("/products/{product_id}", tags=["Update Product details"])
async def update_product(id: int, ProductCreateUpdate: ProductCreateUpdate, session: AsyncSession = Depends(get_session)):
    try:
        queryset_result = await session.get(Product, id)
        if queryset_result:
            queryset_result.name=ProductCreateUpdate.name
            queryset_result.description=ProductCreateUpdate.description
            queryset_result.price=ProductCreateUpdate.price
            queryset_result.suplier_id=ProductCreateUpdate.suplier_id
            session.add(queryset_result)
            await session.commit()
            await session.refresh(queryset_result)
            response_data = ResponseModel(status= "OK", data={"id" : queryset_result.id}, message="Record updated Successfully")
            status_code = 200
        else:
            response_data = ResponseModel(status= "NotOK", data={"error" : "invalid Record id"}, message="Record Not Exist")
            status_code = 400
    except Exception as e:
        status_code = 500
        response_data = ResponseModel(status= "NotOK", data= {"error" :  str(e)}, message="Something went wrong")
    return JSONResponse(status_code=status_code, content=response_data.dict())


@app.get("/customers", tags=["List Customers"], response_model=ResponseModel)
async def list_suppliers(session: AsyncSession = Depends(get_session)):
    try:
        queryset_result = await session.execute(select(Customer))
        result = [each.json() for each in queryset_result.scalars().all()]
        response_data = ResponseModel(status= "OK", data={"result" : result}, message=f"Records Total: {len(result)}")
        status_code = 200
    except Exception as e:
        status_code = 500
        response_data = ResponseModel(status= "NotOK", data= {"error" :  str(e)}, message="Something went wrong")
    return JSONResponse(status_code=status_code, content=response_data.dict())

@app.get("/customers/{customer_id}", tags=["get Customer details"], response_model=ResponseModel)
async def get_customer(customer_id:int,session: AsyncSession = Depends(get_session)):
    try:
        statement = select(Customer).where(Customer.id == customer_id)
        result = (await session.exec(statement)).first()
        if result:
            response_data = ResponseModel(status= "OK", data={"result" : result.json()}, message="1 Record found")
            status_code = 200
        else:
            response_data = ResponseModel(status= "NotOK", data= {"error" : "invalid Record Id"}, message=f"No Records found")
            status_code = 400
    except Exception as e:
        response_data = ResponseModel(status= "NotOK", data= {"error" :  str(e)}, message="Something went wrong")
        status_code = 500
    return JSONResponse(status_code=status_code, content=response_data.dict())

@app.post("/customers", tags=["create new Customer"], response_model=ResponseModel)
async def create_customer(CustomerCreateUpdate: CustomerCreateUpdate, session: AsyncSession = Depends(get_session)):
    try:
        statement = select(Customer).where(Customer.name == CustomerCreateUpdate.name)
        results = await session.exec(statement)
        if len(results.all()) > 0:
            response_data = ResponseModel(status= "NotOK", data={"error" :  CustomerCreateUpdate.name}, message=f"Record already exists with name field value as '{suppliderCreate.name}'")
            status_code = 400
        else:
            supplier_cls = Supplier(name=CustomerCreateUpdate.name, contact_info=CustomerCreateUpdate.contact_info)
            session.add(supplier_cls)
            await session.commit()
            await session.refresh(supplier_cls)
            response_data = ResponseModel(status= "OK", data={"id" : supplier_cls.id}, message="Record Created Successfully")
            status_code = 201
    except Exception as e:
        status_code = 500
        response_data = ResponseModel(status= "NotOK", data= {"error" :  str(e)}, message="Something went wrong")
    return JSONResponse(status_code=status_code, content=response_data.dict())

@app.delete("/customers/{customer_id}", tags=["delete Customer details"], response_model=ResponseModel)
async def delete_customer(customer_id:int,session: AsyncSession = Depends(get_session)):
    try:
        statement = select(Customer).where(Customer.id == customer_id)
        result = (await session.exec(statement))
        await session.delete(result.one())
        if result:
            response_data = ResponseModel(status= "OK", data={"result" : "Record Deleted Successfully"}, message="Record Deleted Successfully")
            status_code = 200
        else:
            response_data = ResponseModel(status= "NotOK", data= {"error" : "invalid Record Id"}, message=f"No Records found")
            status_code = 400
    except Exception as e:
        response_data = ResponseModel(status= "NotOK", data= {"error" :  str(e)}, message="Something went wrong")
        status_code = 500
    return JSONResponse(status_code=status_code, content=response_data.dict())

@app.put("/customers/{customer_id}", tags=["Update Customer details"])
async def update_customer(customer_id: int, CustomerCreateUpdate: CustomerCreateUpdate, session: AsyncSession = Depends(get_session)):
    try:
        queryset_result = await session.get(Customer, customer_id)
        if queryset_result:
            queryset_result.name=CustomerCreateUpdate.name
            queryset_result.contact_info=CustomerCreateUpdate.contact_info
            session.add(queryset_result)
            await session.commit()
            await session.refresh(queryset_result)
            response_data = ResponseModel(status= "OK", data={"id" : queryset_result.id}, message="Record updated Successfully")
            status_code = 200
        else:
            response_data = ResponseModel(status= "NotOK", data={"error" : "invalid Record id"}, message="Record Not Exist")
            status_code = 400
    except Exception as e:
        status_code = 500
        response_data = ResponseModel(status= "NotOK", data= {"error" :  str(e)}, message="Something went wrong")
    return JSONResponse(status_code=status_code, content=response_data.dict())

@app.get("/order_status", tags=["List Order Status"], response_model=ResponseModel)
async def list_order_status(session: AsyncSession = Depends(get_session)):
    try:
        queryset_result = await session.execute(select(OrderStatus))
        result = [each.json() for each in queryset_result.scalars().all()]
        response_data = ResponseModel(status= "OK", data={"result" : result}, message=f"Records Total: {len(result)}")
        status_code = 200
    except Exception as e:
        status_code = 500
        response_data = ResponseModel(status= "NotOK", data= {"error" :  str(e)}, message="Something went wrong")
    return JSONResponse(status_code=status_code, content=response_data.dict())

@app.get("/order_status/{id}", tags=["get Order Status details"], response_model=ResponseModel)
async def get_order_status(id:int,session: AsyncSession = Depends(get_session)):
    try:
        statement = select(OrderStatus).where(Customer.id == id)
        result = (await session.exec(statement)).first()
        if result:
            response_data = ResponseModel(status= "OK", data={"result" : result.json()}, message="1 Record found")
            status_code = 200
        else:
            response_data = ResponseModel(status= "NotOK", data= {"error" : "invalid Record Id"}, message=f"No Records found")
            status_code = 400
    except Exception as e:
        response_data = ResponseModel(status= "NotOK", data= {"error" :  str(e)}, message="Something went wrong")
        status_code = 500
    return JSONResponse(status_code=status_code, content=response_data.dict())

@app.post("/order_status", tags=["create new Order Status"], response_model=ResponseModel)
async def create_order_status(OrderStatusCreateUpdate: OrderStatusCreateUpdate, session: AsyncSession = Depends(get_session)):
    try:
        statement = select(OrderStatus).where(OrderStatus.name == OrderStatusCreateUpdate.name)
        results = await session.exec(statement)
        if len(results.all()) > 0:
            response_data = ResponseModel(status= "NotOK", data={"error" :  OrderStatusCreateUpdate.name}, message=f"Record already exists with name field value as '{suppliderCreate.name}'")
            status_code = 400
        else:
            supplier_cls = Supplier(name=OrderStatusCreateUpdate.name)
            session.add(supplier_cls)
            await session.commit()
            await session.refresh(supplier_cls)
            response_data = ResponseModel(status= "OK", data={"id" : supplier_cls.id}, message="Record Created Successfully")
            status_code = 201
    except Exception as e:
        status_code = 500
        response_data = ResponseModel(status= "NotOK", data= {"error" :  str(e)}, message="Something went wrong")
    return JSONResponse(status_code=status_code, content=response_data.dict())

@app.put("/order_status/{id}", tags=["Update Order Status details"])
async def update_orderstatus(id: int, OrderStatusCreateUpdate: OrderStatusCreateUpdate, session: AsyncSession = Depends(get_session)):
    try:
        queryset_result = await session.get(OrderStatus, id)
        if queryset_result:
            queryset_result.name=OrderStatusCreateUpdate.name
            session.add(queryset_result)
            await session.commit()
            await session.refresh(queryset_result)
            response_data = ResponseModel(status= "OK", data={"id" : queryset_result.id}, message="Record updated Successfully")
            status_code = 200
        else:
            response_data = ResponseModel(status= "NotOK", data={"error" : "invalid Record id"}, message="Record Not Exist")
            status_code = 400
    except Exception as e:
        status_code = 500
        response_data = ResponseModel(status= "NotOK", data= {"error" :  str(e)}, message="Something went wrong")
    return JSONResponse(status_code=status_code, content=response_data.dict())

@app.get("/orders", tags=["List Orders"], response_model=ResponseModel)
async def list_orders(session: AsyncSession = Depends(get_session)):
    try:
        queryset_result = await session.execute(select(Product))
        result = [each.json() for each in queryset_result.scalars().all()]
        response_data = ResponseModel(status= "OK", data={"result" : result}, message=f"Records Total: {len(result)}")
        status_code = 200
    except Exception as e:
        status_code = 500
        response_data = ResponseModel(status= "NotOK", data= {"error" :  str(e)}, message="Something went wrong")
    return JSONResponse(status_code=status_code, content=response_data.dict())

@app.get("/orders/{orders_id}", tags=["get Order details"], response_model=ResponseModel)
async def get_order(orders_id:int,session: AsyncSession = Depends(get_session)):
    try:
        statement = select({Orders}).where(Orders.id == orders_id)
        result = (await session.exec(statement)).first()
        if result:
            response_data = ResponseModel(status= "OK", data={"result" : result.json()}, message="1 Record found")
            status_code = 200
        else:
            response_data = ResponseModel(status= "NotOK", data= {"error" : "invalid Record Id"}, message=f"No Records found")
            status_code = 400
    except Exception as e:
        response_data = ResponseModel(status= "NotOK", data= {"error" :  str(e)}, message="Something went wrong")
        status_code = 500
    return JSONResponse(status_code=status_code, content=response_data.dict())

@app.post("/orders", tags=["create new Order"], response_model=ResponseModel)
async def create_order(OrderCreateUpdate: OrderCreateUpdate, session: AsyncSession = Depends(get_session)):
    try:
        
        order_cls = Orders(order_status_id == OrderCreateUpdate.order_status_id, 
                                         customers_id == OrderCreateUpdate.customers_id,
                                         order_date == OrderCreateUpdate.order_date,
                                         contact_info == OrderCreateUpdate.contact_info)
        session.add(order_cls)
        await session.commit()
        await session.refresh(order_cls)
        for eachitem in OrderCreateUpdate.order_items:
            item_cls = OrdersItems(order_id == eachitem.item_cls.id, 
                                    product_id == eachitem.product_id,
                                    price == eachitem.price,
                                    quantity == eachitem.quantity)
            session.add(item_cls)
            await session.commit()
            await session.refresh(item_cls)
        response_data = ResponseModel(status= "OK", data={"id" : order_cls.id}, message="Record Created Successfully")
        status_code = 201
    except Exception as e:
        status_code = 500
        response_data = ResponseModel(status= "NotOK", data= {"error" :  str(e)}, message="Something went wrong")
    return JSONResponse(status_code=status_code, content=response_data.dict())

@app.put("/orders/{orders_id}", tags=["Update Order details"])
async def update_order(orders_id: int, OrderCreateUpdate: OrderCreateUpdate, session: AsyncSession = Depends(get_session)):
    try:
        queryset_result = await session.get(Orders, orders_id)
        if queryset_result:
            queryset_result.customers_id=OrderCreateUpdate.customers_id
            queryset_result.order_status_id=OrderCreateUpdate.order_status_id
            queryset_result.order_date=OrderCreateUpdate.order_date
            queryset_result.contact_info=OrderCreateUpdate.contact_info
            session.add(queryset_result)
            await session.commit()
            await session.refresh(queryset_result)
            response_data = ResponseModel(status= "OK", data={"id" : queryset_result.id}, message="Record updated Successfully")
            status_code = 200
        else:
            response_data = ResponseModel(status= "NotOK", data={"error" : "invalid Record id"}, message="Record Not Exist")
            status_code = 400
    except Exception as e:
        status_code = 500
        response_data = ResponseModel(status= "NotOK", data= {"error" :  str(e)}, message="Something went wrong")
    return JSONResponse(status_code=status_code, content=response_data.dict())

@app.delete("/orders/{orders_id}", tags=["delete Orders details"], response_model=ResponseModel)
async def delete_Order(orders_id:int,session: AsyncSession = Depends(get_session)):
    try:
        statement = select(Orders).where(Orders.id == orders_id)
        result = (await session.exec(statement))
        await session.delete(result.one())
        if result:
            response_data = ResponseModel(status= "OK", data={"result" : "Record Deleted Successfully"}, message="Record Deleted Successfully")
            status_code = 200
        else:
            response_data = ResponseModel(status= "NotOK", data= {"error" : "invalid Record Id"}, message=f"No Records found")
            status_code = 400
    except Exception as e:
        response_data = ResponseModel(status= "NotOK", data= {"error" :  str(e)}, message="Something went wrong")
        status_code = 500
    return JSONResponse(status_code=status_code, content=response_data.dict())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)