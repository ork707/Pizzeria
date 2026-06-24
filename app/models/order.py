from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    pizza_id = Column(Integer, ForeignKey("pizzas.id"))
    quantity = Column(Integer)
    pizza = relationship("Pizza", back_populates="orders")
    user = relationship("User", back_populates="orders")