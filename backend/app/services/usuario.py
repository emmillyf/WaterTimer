from models.usuario import Usuarios
from models.meta_diaria import MetaDiaria
from datetime import date
from utils.calcular_meta_diaria import calcular_meta_diaria_recomendada
from fastapi import status, HTTPException
from sqlalchemy.exc import IntegrityError 
from sqlalchemy.orm import Session
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_all(db: Session):
    try:
        return db.query(Usuarios).all()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar usuários")

def get_by_id(db: Session, id_user: int):
    try:
        return db.query(Usuarios).filter(Usuarios.id_user==id_user).first()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar usuário")
    
def post_user(db: Session, user_data: dict):
    try:
        try:
            db.query(Usuarios).filter(Usuarios.email == user_data["email"]).first()
        except IntegrityError as e:
            db.rollback()
            if "email" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email já está em uso por outro usuário.")

        novo_usuario = Usuarios(
            nome=user_data.get("nome"),
            email=user_data.get("email"),
            senha=pwd_context.hash(user_data["senha"]),
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
    
def put_user(db: Session, id_user: int, user_data: dict):
    try:
        try: 
            usuario = db.query(Usuarios).filter(Usuarios.id_user == id_user, Usuarios.email == user_data["email"], ).first()
            if not usuario:
                return {"error": f"Usuário ID {id_user} não encontrado"}
        except IntegrityError as e:
            db.rollback()
            if "email" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email já está em uso por outro usuário.")     
        
        usuario.nome = user_data.get("nome", usuario.nome)
        usuario.email = user_data.get("email", usuario.email)
        usuario.idade = user_data.get("idade", usuario.idade)
        usuario.peso = user_data.get("peso", usuario.peso)
        usuario.dorme_por_dia = user_data.get("dorme_por_dia", usuario.dorme_por_dia)
        usuario.horario_dormir = user_data.get("horario_dormir", usuario.horario_dormir)
        usuario.criado_em = user_data.get("criado_em", usuario.criado_em)
        usuario.capacidade_garrafa_ml = user_data.get("capacidade_garrafa_ml", usuario.capacidade_garrafa_ml)

        if "senha" in user_data:
            usuario.senha = pwd_context.hash(user_data["senha"])

        db.add(usuario)
        db.commit()
        db.refresh(usuario)         
        return usuario
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
    
def delete_user_by_id(db: Session, id_user: int):
    try:
        usuario = db.query(Usuarios).filter(Usuarios.id_user == id_user).first()
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        db.delete(usuario)
        db.commit()
        return {"message": f"Usuário {id_user} removido com sucesso!"}
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=('Erro ao detelar usuários'))