from fastapi import APIRouter
from .usuario import router as usuarios_router

main_router = APIRouter()

main_router.include_router(
    usuarios_router,
    tags=["Usuários"]
)
