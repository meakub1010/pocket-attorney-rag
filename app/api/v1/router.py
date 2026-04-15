from fastapi import APIRouter

from app.api.v1.endpoints import query, health

api_router = APIRouter()

api_router.include_router(
    query.router,
    prefix="/query",
    tags=["query"]
)


api_router.include_router(
    health.router,
    prefix="/health",
    tags=["health"]
)