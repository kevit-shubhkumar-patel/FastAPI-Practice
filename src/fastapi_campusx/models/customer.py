from pydantic import BaseModel, EmailStr, Field
from typing import Literal


class CustomerCreate(BaseModel):
    id: int = Field(alias="_id")
    name: str = Field(min_length=2)
    email: EmailStr
    city: str
    membership: Literal["bronze", "silver", "gold"]


class CustomerUpdate(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    city: str
    membership: Literal["bronze", "silver", "gold"]