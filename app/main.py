from fastapi import FastAPI
from app.routers import pizzas, orders, users
from app.database import engine
from app.models.pizza import Base
from app.models.pizza import Pizza
from app.models.order import Order
from app.models.user import User


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(pizzas.router)
app.include_router(orders.router)
app.include_router(users.router)

@app.get("/")
def home():
    return {"message": "Pizza Heart!"}