from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemas.usuario import Token
from database.conexao import get_db
from utils.security import criar_acesso_token
import services.usuario as service

router = APIRouter(
)

@router.post("/usuarios/login", response_model=Token)
async def login_usuario(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        logar_usuario = service.login_user(db, email=form_data.username, senha=form_data.password)
        token = criar_acesso_token(data={"sub": logar_usuario.email})
        return {"acess_token": token, "token_type": "bearer"}
    except ValueError as e:
        print(f"{e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro{e}")