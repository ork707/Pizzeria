from pydantic import BaseModel

class PizzaInfo(BaseModel):
    id: int
    name: str
    price: int

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    user_id: int
    pizza_id: int
    quantity: int

class OrderResponse(BaseModel):
    id: int
    quantity: int
    pizza: PizzaInfo

    class Config:
        from_attributes = True