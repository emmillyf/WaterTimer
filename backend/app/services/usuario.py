from models.usuario import Usuarios
from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_all(db: Session):
    try:
        return db.query(Usuarios).all()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar usuários"
        )

def get_by_id(db: Session, id_usuario: int):
    try:
        return db.query(Usuarios).filter(Usuarios.id_user==id_usuario).first()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar usuário"
        )


def post_user(db: Session, user_data: dict):
    try:
        verifica_existencia = db.query(Usuarios).filter(Usuarios.nome == user_data["nome"]).first()
        if verifica_existencia:
            return {"error": "Nome já cadastrado"}

        new_user = Usuarios(
            nome=user_data.get("nome"),
            senha=pwd_context.hash(user_data["senha"]),
            idade=user_data.get("idade"),
            peso=user_data.get("peso"),
            horario_acordar=user_data.get("horario_acordar"),
            horario_dormir=user_data.get("horario_dormir"),
            capacidade_garrafa_ml=user_data.get("capacidade_garrafa_ml")
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)   
        return new_user

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar usuário"
        )

def put_user(db: Session, user_id: int, user_data: dict):
    try:
        usuario = db.query(Usuarios).filter(Usuarios.id_user == user_id).first()
        if not usuario:
            return {"error": f"Usuário ID {user_id} não encontrado"}

        if "nome" in user_data and user_data["nome"] != usuario.nome:
            existing_user = db.query(Usuarios).filter(
                Usuarios.nome == user_data["nome"],
                Usuarios.id_user != user_id
            ).first()
            if existing_user:
                return {"error": "Nome já está em uso por outro usuário"}

        usuario.nome = user_data.get("nome", usuario.nome)
        usuario.idade = user_data.get("idade", usuario.idade)
        usuario.peso = user_data.get("peso", usuario.peso)
        usuario.horario_acordar = user_data.get("horario_acordar", usuario.horario_acordar)
        usuario.horario_dormir = user_data.get("horario_dormir", usuario.horario_dormir)
        usuario.criado_em = user_data.get("criado_em", usuario.criado_em)
        usuario.capacidade_garrafa_ml = user_data.get("capacidade_garrafa_ml", usuario.capacidade_garrafa_ml)

        if "senha" in user_data:
            usuario.senha = pwd_context.hash(user_data["senha"])

        db.commit()
        db.refresh(usuario)
        return usuario
    
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=('Erro ao atualizar usuário')
        )
    
def delete_user(db: Session):
    try:
        deletados = db.query(Usuarios).delete()
        db.commit()
        return {"message": f"{deletados} Usuários foram removidos com sucesso"}
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=('Erro ao atualizar usuário')
        )
    
def delete_user_by_id(db: Session, id: int):
    try:
        usuario = db.query(Usuarios).filter(Usuarios.id_user == id).first()
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        db.delete(usuario)
        db.commit()
        return {"message": f"Usuário {id} removido com sucesso!"}
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=('Erro ao atualizar usuário')
        )