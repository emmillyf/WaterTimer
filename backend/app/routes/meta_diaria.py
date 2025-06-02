from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.conexao import get_db
import services.meta_diaria as service
from schemas.usuario import UsuarioMetaRequest
from schemas.meta_diaria import MetaDiaria, MetaDiariaResponse

router = APIRouter(
)

@router.get("/usuarios/metas", response_model=list[MetaDiariaResponse])
async def buscar_metas_usuarios(db: Session = Depends(get_db)):
    try:
        usuarios = service.get_all(db)
        return usuarios
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
@router.post("/cadastrar/{id_user}/meta", response_model=MetaDiaria, status_code=status.HTTP_201_CREATED)
async def criar_usuario_meta(user_data: UsuarioMetaRequest, id_user:int, db: Session = Depends(get_db)):
    try:
        criando_meta = service.post_meta(db, user_data.model_dump(), id_user)

        if isinstance(criando_meta, dict) and "error" in criando_meta:
            error_msg = criando_meta["error"]
            if "Meta já cadastrada" in error_msg:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT)
            else:
                print(error_msg)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST)
        return criando_meta
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@router.put("/usuarios/{id_user}/registro_hidratacao", response_model=MetaDiaria)
async def atualizar_consumo_usuario(id_user: int, ml_consumida: int, db: Session = Depends(get_db)):
    try:
        atualizando_meta = service.put_consumo_diario(db, id_user, ml_consumida)
        return atualizando_meta
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Erro inesperado ao atualizar meta do usuário: {str(e)}")
    
@router.delete("/usuarios/metas")
async def deletar_todas_metas(db: Session = Depends(get_db)):
    try:
        service.delete_metas(db)
        return {"message": "Metas deletadas com sucesso"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e))

@router.delete("/usuarios/{id_user}/meta")
async def deletar_usuario_id(id_user: int, db: Session = Depends(get_db)):
    try:
        service.delete_meta_by_id(db, id_user)
        return {"message": "Meta do usuário foi deletada com sucesso"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e))