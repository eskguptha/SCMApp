# Supply Chain Management System(SCM App)

The objective of this assignment is to evaluate the candidate's proficiency in developing a RESTful API using FastAPI. The candidate should demonstrate their ability to design, develop, test, and document a web API, handle complex API functionalities, manage intricate database interactions, and implement security features.

1. Create Virtualenv

goto command prompt and run below commands
`python -m venv scm_env
scm_env\Scripts\activate
python.exe -m pip install --upgrade pip
`
2. Install Pip packages
`
pip install -r requirements.txt
`

3. initialize alembic 

`alembic init alembic
`

4. After initialization it will create a file name “alembic.ini”, now open this file and you will get “sqlalchemy.url” so here you have to give your SQLAlchemy URL is all that’s needed but without commas

In my case, because I am using SQLite dB

`sqlalchemy.url = sqlite+aiosqlite:///database.db`

5. env.py settings 
`from sqlmodel import SQLModel
from models import *
->You can set a variable (render_as_batch=True) in the env.py file created with the initial migation.
context.configure(
    connection=connection,
    target_metadata=target_metadata,
    render_as_batch=True
)`


6. Now, you have to just run the migrations like

`alembic init -t async migrations 
alembic revision --autogenerate -m "init"

then

alembic upgrade head
`

8. Run existing project directly from Github URL

`
go to command prompt and run below command
git clone https://github.com/eskguptha/SCMApp.git
`
9. Run Application
`python main.py
or 
uvicorn app:main --reload

10. goto browser open below URL

`http://127.0.0.1:8000`
`
11. Swager
`
http://127.0.0.1:8000/docs
`


# Assignment: Developing a RESTful API for a Supply Chain Management System using FastAPI
`
##Objective:
The objective of this assignment is to evaluate the candidate's proficiency in developing a RESTful API using FastAPI. The candidate should demonstrate their ability to design, develop, test, and document a web API, handle complex API functionalities, manage intricate database interactions, and implement security features.
 
## Project Description:
You are required to create a RESTful API for a supply chain management system. The system should allow users to manage products, suppliers, customers, orders, and shipments. The API should support CRUD operations for each of these entities and include additional functionalities such as inventory tracking, order fulfillment, and generating supply chain reports.
 
## Requirements:
Setup and Configuration:
 
Use FastAPI to create the API.
Use SQLAlchemy as the ORM for database interactions.
Use PostgreSQL for the database.
Include Pydantic models for data validation.
Include pytest for testing.
Implement authentication using OAuth2 with JWT tokens.
Use Alembic for database migrations.
Entities and Relationships:
 
Product:
 
id (Primary Key)
name
description
price
supplier_id (Foreign Key referencing Supplier)
stock (Integer indicating available quantity)
Supplier:
 
id (Primary Key)
name
contact_info
products (One-to-Many relationship with Product)
Customer:
 
id (Primary Key)
name
contact_info
orders (One-to-Many relationship with Order)
Order:
 
id (Primary Key)
customer_id (Foreign Key referencing Customer)
order_date
status (Pending, Fulfilled, Cancelled)
order_items (One-to-Many relationship with OrderItem)
OrderItem:
 
id (Primary Key)
order_id (Foreign Key referencing Order)
product_id (Foreign Key referencing Product)
quantity
price
Shipment:
 
id (Primary Key)
order_id (Foreign Key referencing Order)
shipment_date
delivery_date
status (Shipped, In Transit, Delivered, Returned)
API Endpoints:
 
 
Customers:
 
GET /customers: List all customers
POST /customers: Create a new customer
GET /customers/{customer_id}: Retrieve a customer by ID
PUT /customers/{customer_id}: Update a customer by ID
DELETE /customers/{customer_id}: Delete a customer by ID
Orders:
 
GET /orders: List all orders
POST /orders: Create a new order
GET /orders/{order_id}: Retrieve an order by ID
PUT /orders/{order_id}: Update an order by ID
DELETE /orders/{order_id}: Delete an order by ID
PATCH /orders/{order_id}/status: Update the status of an order
GET /orders/{order_id}/items: List all items in an order
 
### Database Models:
 
Create SQLAlchemy models for Product, Supplier, Customer, Order, OrderItem, and Shipment.
Ensure proper relationships and constraints are set up in the database schema.
Data Validation:
 
Use Pydantic models for request and response validation.
Authentication and Authorization:
 
Implement OAuth2 authentication with JWT tokens.
Protect sensitive endpoints so only authenticated users can access them.
Additional Functionalities:
 
Inventory Tracking: Track and log every inventory movement (addition, removal) for audit purposes.
Order Fulfillment: Implement logic to fulfill an order (reduce stock, change status).
Shipment Tracking: Track the status and progress of shipments.
Supply Chain Reports: Generate reports that summarize order status, inventory levels, shipment status, and supplier performance.
Testing:
 
Write unit tests for each endpoint using pytest.
Include tests for authentication and authorization.
Include tests for data validation and error handling.
Documentation:
 
## Use Swagger UI provided by FastAPI for API documentation.
Include clear and concise documentation for each endpoint, including request and response examples.
## Submission:
 
Provide a GitHub repository link with the complete codebase.
Include a README file with setup instructions, how to run the application, and how to run the tests.

`

# Testing
run below command to run test cases
`
pytest
`
