from fastapi import FastAPI, Path, Query,HTTPException
from contextlib import asynccontextmanager
from pymongo import AsyncMongoClient


MONGODB_URL = "mongodb://localhost:27017/"
DATABASE_NAME = "mongodb_task"

@asynccontextmanager
async def lifespan(app : FastAPI):
    client = AsyncMongoClient(MONGODB_URL)

    app.state.mongodb_client = client
    app.state.database = client[DATABASE_NAME]

    try:
        await client.admin.command("ping")
        print("Connected Successfully")

        yield
    finally:
        await client.close()
    
app = FastAPI(lifespan=lifespan)

@app.get("/products")
async def get_products():
    collection = app.state.database["products"]

    products = await collection.find().to_list(length = 100)

    for product in products:
        product["_id"] = str(product["_id"])
    return products

@app.get("/sort_by_price")
async def sort_by_price(
    sort_by: str = Query(
        default="asc",
        description="Sort by price: asc or desc"
    )
):
    collection = app.state.database["products"]

    sort_order = 1 if sort_by.lower() == "asc" else -1

    if sort_by.lower() not in ("asc", "desc"):
        raise HTTPException(
            status_code=400,
            detail="sort_by must be 'asc' or 'desc'"
        )

    products = await collection.find().sort(
        "price", sort_order
    ).to_list(length=100)

    for product in products:
        product["_id"] = str(product["_id"])

    return products

@app.get("/orders")
async def get_orders():
    collection = app.state.database["orders"]

    orders  = await collection.find().to_list(length = 100)
    return orders

# Path Params
@app.get("/customers/{customer_id}")
async def get_customers_by_id(customer_id : int = Path(...,description="The ID of customer in DB", example=101)):
    
    collection = app.state.database["customers"]

    customer = await collection.find_one({"_id" : customer_id})
    return customer

