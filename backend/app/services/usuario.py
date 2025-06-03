from models.usuario import Usuarios
from fastapi import status, HTTPException, Depends
from sqlalchemy.exc import IntegrityError 
from sqlalchemy.orm import Session
from utils.security import (get_senha_hash, 
verificar_senha, get_user_atual)

def get_all(db: Session):
    usuarios = db.query(Usuarios).all()
    if not usuarios:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Erro ao buscar usuarios")
    return usuarios

def get_by_id(db: Session, id_user: int):
        usuario = db.query(Usuarios).filter(Usuarios.id_user==id_user).first()
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Erro ao buscar usuário")
        return usuario
    
def post_user(db: Session, user_data: dict):
    try:
        usuario = db.query(Usuarios).filter(Usuarios.email == user_data["email"]).first()
        if usuario:
            if usuario.username == usuario.nome:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail='Esse nome já existe',
                )
            elif usuario.email == usuario.email:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail='Esse email já existe',
                )
        
        novo_usuario = Usuarios(
            nome=user_data.get("nome"),
            email=user_data.get("email"),
            senha=get_senha_hash(user_data["senha"]),
            idade=user_data.get("idade"),
            peso=user_data.get("peso"),
            dorme_por_dia=user_data.get("dorme_por_dia"),
            horario_dormir=user_data.get("horario_dormir"),
            capacidade_garrafa_ml=user_data.get("capacidade_garrafa_ml"))

        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
        return novo_usuario
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro inesperado ao criar usuário: {str(e)}")

def login_user(db: Session, email: str, senha: str):
    try:
        usuario = db.query(Usuarios).filter(Usuarios.email == email).first()

        if not usuario or not verificar_senha(senha, usuario.senha):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas"
            )

        return usuario
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro inesperado ao Logar usuário: {str(e)}")

def put_user(db: Session, id_user: int, user_data: dict, current_user: Usuarios = Depends(get_user_atual)):
    try:
        if current_user.id_user != id_user :
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Usuário não autorizado'
            )

        current_user.nome = user_data.get("nome", current_user.nome)
        current_user.email = user_data.get("email", current_user.email)
        current_user.idade = user_data.get("idade", current_user.idade)
        current_user.peso = user_data.get("peso", current_user.peso)
        current_user.dorme_por_dia = user_data.get("dorme_por_dia", current_user.dorme_por_dia)
        current_user.horario_dormir = user_data.get("horario_dormir", current_user.horario_dormir)
        current_user.capacidade_garrafa_ml = user_data.get("capacidade_garrafa_ml", current_user.capacidade_garrafa_ml)

        if "senha" in user_data:
            current_user.senha = get_senha_hash(user_data["senha"])

        db.add(current_user)
        db.commit()
        db.refresh(current_user)         
        return current_user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro inesperado ao atualizar usuário: {str(e)}")
    
def delete_user(db: Session):
    try:
        deletados = db.query(Usuarios).delete()
        db.commit()
        return {"message": f"{deletados} Usuários foram removidos com sucesso"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar usuários {str(e)}")
    
def delete_user_by_id(db: Session, id_user: int, current_user: Usuarios = Depends(get_user_atual)):
    try:
        if current_user.id_user != id_user :
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail='Usuário não autorizado'
                    )
        
        usuario = current_user.id_user
        db.delete(usuario)
        db.commit()
        return {"message": f"Usuário {id_user} removido com sucesso!"}
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=('Erro ao deletar usuários'))