from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    id: str = Field(alias="_id")
    name: str = Field(min_length=2)
    category: str
    price: float = Field(gt=0)
    stock: int = Field(ge=0)


class ProductUpdate(BaseModel):
    name: str = Field(min_length=2)
    category: str
    price: float = Field(gt=0)
    stock: int = Field(ge=0)