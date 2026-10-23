from fastapi import APIRouter, Depends, HTTPException
from fastapi_campusx.database import get_database
from fastapi_campusx.models.customer import CustomerCreate, CustomerUpdate

router = APIRouter(prefix="/customers", tags=["Customers"])


# 1. CREATE a customer
@router.post("/")
async def create_customer(
    customer: CustomerCreate,
    database=Depends(get_database)
):
    collection = database["customers"]

    customer_data = customer.model_dump(by_alias=True)

    await collection.insert_one(customer_data)

    return {"message": "Customer created successfully"}


# 2. GET all customers
@router.get("/")
async def get_customers(database=Depends(get_database)):
    collection = database["customers"]

    customers = await collection.find().to_list(length=100)

    return customers


# 3. GET one customer
@router.get("/{customer_id}")
async def get_customer(
    customer_id: int,
    database=Depends(get_database)
):
    collection = database["customers"]

    customer = await collection.find_one({"_id": customer_id})

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


# 4. UPDATE a customer
@router.put("/{customer_id}")
async def update_customer(
    customer_id: int,
    customer: CustomerUpdate,
    database=Depends(get_database)
):
    collection = database["customers"]

    customer_data = customer.model_dump()

    result = await collection.update_one(
        {"_id": customer_id},
        {"$set": customer_data}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return {"message": "Customer updated successfully"}


# 5. DELETE a customer
@router.delete("/{customer_id}")
async def delete_customer(
    customer_id: int,
    database=Depends(get_database)
):
    collection = database["customers"]

    result = await collection.delete_one({"_id": customer_id})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return {"message": "Customer deleted successfully"}