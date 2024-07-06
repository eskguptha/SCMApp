python -m venv scm_env
scm_env\Scripts\activate
python.exe -m pip install --upgrade pip
pip install -r requirements.txt

https://testdriven.io/blog/fastapi-sqlmodel/

1. initialize alembic

`alembic init alembic`

2. After initialization it will create a file name “alembic.ini”, now open this file and you will get “sqlalchemy.url” so here you have to give your SQLAlchemy URL is all that’s needed but without commas

In my case, because I am using SQLite dB

`sqlalchemy.url = sqlite+aiosqlite:///database.db`

3. env.py 

`from sqlmodel import SQLModel
from models import *
->You can set a variable (render_as_batch=True) in the env.py file created with the initial migation.
context.configure(
    connection=connection,
    target_metadata=target_metadata,
    render_as_batch=True
)`


4. Now, you have to just run the migrations like

`alembic init -t async migrations 
alembic revision --autogenerate -m "init"

then

alembic upgrade head
`