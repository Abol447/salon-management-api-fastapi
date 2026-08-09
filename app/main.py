from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine
from app.api.role_router import router as role_router
from app.api.user_route import router as user_router
from app.api.auth_router import router as auth_router
from app.api.discount_router import router as discount_router
from app.api.customer_router import router as customer_router
from app.api.services_router import router as service_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():

    with engine.connect() as connection:
        return {"message": "Database connected"}


app.include_router(role_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(customer_router)
app.include_router(discount_router)
app.include_router(service_router)
