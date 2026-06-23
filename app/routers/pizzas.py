from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.database import SessionLocal
from app.models.pizza import Pizza
from app.schemas.pizza import PizzaCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/pizzas")
def get_pizzas(db: Session = Depends(get_db)):
    return db.query(Pizza).all()

@router.post("/pizzas")
def create_pizza(
    pizza: PizzaCreate,
    db: Session = Depends(get_db)
):
    new_pizza = Pizza(
        name=pizza.name,
        price=pizza.price
    )

    db.add(new_pizza)
    db.commit()
    db.refresh(new_pizza)

    return new_pizza

@router.get("/pizzas/{pizza_id}")
def get_pizza(
    pizza_id: int,
    db: Session = Depends(get_db)
):
    pizza = db.query(Pizza).filter(
        Pizza.id == pizza_id
    ).first()

    if pizza is None:
        raise HTTPException(
            status_code=404,
            detail="Pizza not found"
        )

    return pizza

@router.put("/pizzas/{pizza_id}")
def update_pizza(
    pizza_id: int,
    pizza_data: PizzaCreate,
    db: Session = Depends(get_db)
):
    pizza = db.query(Pizza).filter(
        Pizza.id == pizza_id
    ).first()

    if pizza is None:
        raise HTTPException(
            status_code=404,
            detail="Pizza not found"
        )

    pizza.name = pizza_data.name
    pizza.price = pizza_data.price

    db.commit()
    db.refresh(pizza)

    return pizza

@router.delete("/pizzas/{pizza_id}")
def delete_pizza(
    pizza_id: int,
    db: Session = Depends(get_db)
):
    pizza = db.query(Pizza).filter(
        Pizza.id == pizza_id
    ).first()

    if pizza is None:
        raise HTTPException(
            status_code=404,
            detail="Pizza not found"
        )

    db.delete(pizza)
    db.commit()

    return {
        "message": "Pizza deleted"
    }