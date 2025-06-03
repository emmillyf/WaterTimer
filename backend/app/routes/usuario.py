from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.conexao import get_db
from utils.security import get_user_atual
import services.usuario as service
from schemas.usuario import (UsuarioResponse, 
    UsuarioBase, 
    UsuarioUpdate)

router = APIRouter(
)

@router.get("/usuarios", response_model=list[UsuarioResponse])
async def buscar_usuarios(db: Session = Depends(get_db)):
    try:
        usuarios = service.get_all(db)
        print("📦 Resposta que será retornada:", usuarios)
        return usuarios
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/usuarios/{id_user}", response_model=UsuarioResponse)
async def buscar_usuario_id(id_user:int, db: Session = Depends(get_db)):
    try:
        usuario = service.get_by_id(db, id_user)
        print("📦 Resposta que será retornada:", usuario)
        return usuario
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e))

@router.post("/cadastrar", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def criar_usuario(user_data: UsuarioBase, db: Session = Depends(get_db)):
    try:
        criando_usuario = service.post_user(db, user_data.model_dump())

        if isinstance(criando_usuario, dict) and "error" in criando_usuario:
            error_msg = criando_usuario["error"]
            if "Email já cadastrado" in error_msg:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email já cadastrado no sistema")
            else:
                print(error_msg)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST)
        return criando_usuario
    
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@router.put("/usuarios/{id_user}", response_model=UsuarioUpdate)
async def atualizar_usuario(id_user: int, user_data: UsuarioUpdate,
db: Session = Depends(get_db), current_user: UsuarioUpdate = Depends(get_user_atual)):
    try:
        atualizando_usuario = service.put_user(db, id_user, user_data.model_dump(), current_user)
        return atualizando_usuario
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=('Erro ao atualizar usuário'))

@router.delete("/usuarios")
async def deletar_todos_usuarios(db: Session = Depends(get_db)):
    try:
        service.delete_user(db)
        return {"message": "Usuários deletados com sucesso"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e))

@router.delete("/usuarios/{id_user}")
async def deletar_usuario_id(id_user: int, db: Session = Depends(get_db), current_user: UsuarioBase = Depends(get_user_atual)):
    try:
        service.delete_user_by_id(db, id_user, current_user)
        return {"message": "Usuário deletado com sucesso"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e))

