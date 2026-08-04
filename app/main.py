from fastapi import FastAPI
from app.db.database import engine
from app.api.role_router import router as role_router
from app.api.user_route import router as user_router
from app.api.auth_router import router as auth_router

app = FastAPI()


@app.get("/")
def root():

    with engine.connect() as connection:
        return {
            "message": "Database connected"
        }

app.include_router(role_router)
app.include_router(user_router)
app.include_router(auth_router)

