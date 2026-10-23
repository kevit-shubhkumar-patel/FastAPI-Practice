from fastapi import FastAPI

from fastapi_campusx.database import lifespan
from fastapi_campusx.routes.customers import router as customers_router
from fastapi_campusx.routes.products import router as products_router
from fastapi_campusx.routes.orders import router as orders_router


app = FastAPI(
    title="MongoDB CRUD API",
    lifespan=lifespan
)


app.include_router(customers_router)
app.include_router(products_router)
app.include_router(orders_router)


@app.get("/")
async def home():
    return {"message": "API is running successfully"}