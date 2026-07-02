from pydantic import BaseModel
from app.schemas.pizza import PizzaResponse


class OrderCreate(BaseModel):
    pizza_id: int
    quantity: int

class OrderResponse(BaseModel):
    id: int
    quantity: int
    pizza: PizzaResponse

    class Config:
        from_attributes = True