from app.routers.user import router as user_router
from fastapi import FastAPI

app = FastAPI(title="User Information Service")

app.include_router(user_router)
