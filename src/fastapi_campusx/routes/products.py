from fastapi import APIRouter, Depends, HTTPException
from fastapi_campusx.models.product import ProductCreate, ProductUpdate
from fastapi_campusx.database import get_database

router = APIRouter(prefix="/products", tags=["Products"])


# 1. CREATE a product
@router.post("/")
async def create_product(
    product: ProductCreate,
    database=Depends(get_database)
):
    collection = database["products"]

    product_data = product.model_dump(by_alias=True)

    await collection.insert_one(product_data)

    return {"message": "Product created successfully"}


# 2. GET all products
@router.get("/")
async def get_products(database=Depends(get_database)):
    collection = database["products"]

    products = await collection.find().to_list(length=100)

    return products


# 3. GET one product
@router.get("/{product_id}")
async def get_product(
    product_id: str,
    database=Depends(get_database)
):
    collection = database["products"]

    product = await collection.find_one({"_id": product_id})

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


# 4. UPDATE a product
@router.put("/{product_id}")
async def update_product(
    product_id: str,
    product: ProductUpdate,
    database=Depends(get_database)
):
    collection = database["products"]

    product_data = product.model_dump()

    result = await collection.update_one(
        {"_id": product_id},
        {"$set": product_data}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return {"message": "Product updated successfully"}


# 5. DELETE a product
@router.delete("/{product_id}")
async def delete_product(
    product_id: str,
    database=Depends(get_database)
):
    collection = database["products"]

    result = await collection.delete_one({"_id": product_id})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return {"message": "Product deleted successfully"}