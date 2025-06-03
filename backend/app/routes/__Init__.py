from fastapi import APIRouter
from .usuario import router as usuarios_router
from .meta_diaria import router as meta_router
from .auth import router as login_router

main_router = APIRouter()

main_router.include_router(
    meta_router,
    tags=["Metas diárias"]
)

main_router.include_router(
    usuarios_router,
    tags=["Usuários"]
)

main_router.include_router(
    login_router,
    tags=["Usuários"]
)