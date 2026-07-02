from pydantic import BaseModel

class PizzaCreate(BaseModel):
    name: str
    price: int

class PizzaResponse(PizzaCreate):
    id: int
    name: str
    price: int

    class Config:
        from_attributes = True