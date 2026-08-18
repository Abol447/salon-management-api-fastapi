from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine
from app.api.role_router import router as role_router
from app.api.user_route import router as user_router
from app.api.auth_router import router as auth_router
from app.api.discount_router import router as discount_router
from app.api.customer_router import router as customer_router
from app.api.services_router import router as service_router
from app.api.appointment_router import router as appointment_router
from app.api.appointmentService_router import router as appointment_service_router
from app.api.salon_router import router as salon_router
from app.api.owner_router import router as owner_router
from app.api.wallet_router import router as wallet_router
from app.api.transaction_route import router as transaction_router
from app.api.discount_usage_router import router as discount_usage_router

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
app.include_router(appointment_router)
app.include_router(appointment_service_router)
app.include_router(salon_router)
app.include_router(owner_router)
app.include_router(wallet_router)
app.include_router(transaction_router)
app.include_router(discount_usage_router)
