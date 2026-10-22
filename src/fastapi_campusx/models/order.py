from pydantic import BaseModel, Field
from typing import Literal


class OrderItem(BaseModel):
    product_id: str
    quantity: int = Field(gt=0)
    price: float = Field(ge=0)


class Payment(BaseModel):
    method: Literal["COD", "UPI", "Card", "Net Banking"]
    status: Literal["pending", "paid", "failed"]


class OrderCreate(BaseModel):
    id: str = Field(alias="_id")
    customer_id: int
    status: Literal[
        "processing",
        "shipped",
        "delivered",
        "cancelled"
    ]
    order_date: str
    items: list[OrderItem] = Field(min_length=1)
    payment: Payment


class OrderUpdate(BaseModel):
    customer_id: int
    status: Literal[
        "processing",
        "shipped",
        "delivered",
        "cancelled"
    ]
    order_date: str
    items: list[OrderItem] = Field(min_length=1)
    payment: Payment