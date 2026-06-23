from pydantic import BaseModel

class PizzaCreate(BaseModel):
    name: str
    price: int

class PizzaResponse(PizzaCreate):
    id: int
