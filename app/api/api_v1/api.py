from fastapi import APIRouter

from app.api.api_v1.endpoints import index, users

api_router = APIRouter()
api_router.include_router(index.router)
api_router.include_router(users.router)
