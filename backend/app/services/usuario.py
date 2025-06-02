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
# FAZER POST SEPARADO PARA A META DIARIA (O CALCULO DA META DIARIA E O REGISTRO DE ATUALIZAÇAO DO USUARIO)
def post_user_meta(db: Session, user_data: dict, user_id: int):
    try:
        try:
            usuario = db.query(Usuarios).filter(Usuarios.id_user == user_id).first()
        except IntegrityError as e:
            db.rollback()
            if "id_user" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Usuário não existe")
            
        peso_atual = user_data.get("peso", usuario.peso)
        idade_atual = user_data.get("idade", usuario.idade)    

        if peso_atual is not None and peso_atual >= 5 and idade_atual is not None:
                try:
                    
                    meta_ml = calcular_meta_diaria_recomendada(
                        peso=peso_atual,
                        idade=idade_atual
                    )
                    
                    nova_meta = MetaDiaria(
                        meta_ml=meta_ml,
                        consumo_atual_ml=0,
                        meta_alcancada=False,
                        id_user=usuario.id_user
                    )

                    db.add(nova_meta)
                    db.commit()
                    db.refresh(nova_meta) 
                    return nova_meta
                except IntegrityError as e:
                        raise HTTPException(
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Erro ao calcular meta para o usuário: {str(e)}")
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro inesperado ao atualizar usuário: {str(e)}")

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
            horario_acordar=user_data.get("horario_acordar"),
            horario_dormir=user_data.get("horario_dormir"),
            capacidade_garrafa_ml=user_data.get("capacidade_garrafa_ml")
        )

        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
        return novo_usuario
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro inesperado ao criar usuário: {str(e)}")

def put_user(db: Session, user_id: int, user_data: dict):
    try:
        meta_diaria = db.query(MetaDiaria).filter(
            MetaDiaria.id_user == user_id).first()
        if not meta_diaria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meta diária não encontrada para o usuário"
            )
        
        usuario = db.query(Usuarios).filter(Usuarios.id_user == user_id, Usuarios.email == user_data["email"], ).first()
        if not usuario:
            return {"error": f"Usuário ID {user_id} não encontrado"}
        elif not usuario:
            return {"error": f"Email já cadastrado"}
                
        peso_antigo = float(usuario.peso)
        idade_antiga = int(usuario.idade)
        
        usuario.nome = user_data.get("nome", usuario.nome)
        usuario.email = user_data.get("email", usuario.email)
        usuario.idade = user_data.get("idade", usuario.idade)
        usuario.peso = user_data.get("peso", usuario.peso)
        usuario.horario_acordar = user_data.get("horario_acordar", usuario.horario_acordar)
        usuario.horario_dormir = user_data.get("horario_dormir", usuario.horario_dormir)
        usuario.criado_em = user_data.get("criado_em", usuario.criado_em)
        usuario.capacidade_garrafa_ml = user_data.get("capacidade_garrafa_ml", usuario.capacidade_garrafa_ml)

        if "senha" in user_data:
            usuario.senha = pwd_context.hash(user_data["senha"])

        peso_atual = float(usuario.peso)
        idade_atual = int(usuario.idade)

        try:
            db.commit()
            db.refresh(usuario)
            
            if (peso_antigo != usuario.peso or idade_antiga != usuario.idade) and \
                peso_atual is not None and peso_atual >= 5 and idade_atual is not None:
                try:
                    
                    atual_ml = meta_diaria.consumo_atual_ml
                    quantidade_ml = meta_diaria.meta_ml

                    atual_ml = max(0, quantidade_ml - atual_ml)  

                    meta_ml = calcular_meta_diaria_recomendada(
                        peso=usuario.peso,
                        idade=usuario.idade
                    )

                    if atual_ml <= 0:
                        meta_diaria.meta_alcancada = True
                    else:
                        meta_diaria.meta_alcancada = False

                    nova_meta = MetaDiaria(
                        meta_ml=meta_ml,
                        consumo_atual_ml=0,
                        meta_alcancada=False,
                        id_user=usuario.id_user
                    )  

                    db.add(nova_meta)
                    db.commit()
                    db.refresh(nova_meta) 

                except ValueError:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=('Erro ao atualizar meta para usuário'))
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return usuario
        except IntegrityError as e:
            db.rollback()
            if "email" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email já está em uso por outro usuário.")
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
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=('Erro ao atualizar usuário'))
    
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
            detail=('Erro ao atualizar usuário'))