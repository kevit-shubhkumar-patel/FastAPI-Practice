from fastapi import APIRouter, Depends, HTTPException
from fastapi_campusx.database import get_database
from fastapi_campusx.models.order import OrderCreate, OrderUpdate

router = APIRouter(prefix="/orders", tags=["Orders"])


# 1. CREATE an order
@router.post("/")
async def create_order(
    order: OrderCreate,
    database=Depends(get_database)
):
    collection = database["orders"]

    order_data = order.model_dump(by_alias=True)

    await collection.insert_one(order_data)

    return {"message": "Order created successfully"}


# 2. GET all orders
@router.get("/")
async def get_orders(database=Depends(get_database)):
    collection = database["orders"]

    orders = await collection.find().to_list(length=100)

    return orders


# 3. GET one order
@router.get("/{order_id}")
async def get_order(
    order_id: str,
    database=Depends(get_database)
):
    collection = database["orders"]

    order = await collection.find_one({"_id": order_id})

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order


# 4. UPDATE an order
@router.put("/{order_id}")
async def update_order(
    order_id: str,
    order: OrderUpdate,
    database=Depends(get_database)
):
    collection = database["orders"]

    order_data = order.model_dump()

    result = await collection.update_one(
        {"_id": order_id},
        {"$set": order_data}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return {"message": "Order updated successfully"}


# 5. DELETE an order
@router.delete("/{order_id}")
async def delete_order(
    order_id: str,
    database=Depends(get_database)
):
    collection = database["orders"]

    result = await collection.delete_one({"_id": order_id})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return {"message": "Order deleted successfully"}