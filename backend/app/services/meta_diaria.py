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
        return db.query(MetaDiaria).all()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar metas diárias")

def get_meta_by_id(db: Session, id_user: int) -> MetaDiaria:
    try:
        return db.query(MetaDiaria).filter(MetaDiaria.id_user==id_user).first()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar meta do usuário")

def get_meta_diaria(db: Session, id_user: int, user_data: dict) -> MetaDiaria:
    try:
        dia_atual = date.today()
        meta_atual = db.query(MetaDiaria).filter(
            MetaDiaria.id_user == id_user,
            MetaDiaria.data == dia_atual
        ).first()

        if meta_atual:
            return meta_atual
        
        try:
            ml_recomendado = post_meta(db, user_data, id_user)
            
            nova_meta_diaria = MetaDiaria(
                quantidade_ml=ml_recomendado,
                consumo_atual_ml=0,
                meta_alcancada=False,
                id_user=id_user,
                data=dia_atual 
            )
            db.add(nova_meta_diaria)
            db.commit()
            db.refresh(nova_meta_diaria)
            return nova_meta_diaria
        except HTTPException as e:
            raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar meta diária para hoje para o usuário {id_user}: {str(e)}"
        )

def post_meta(db: Session, user_data: dict, id_user: int):
    try:
        try:
            usuario = db.query(Usuarios).filter(Usuarios.id_user == id_user).first()
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
                    
                    meta = MetaDiaria(
                        meta_ml=meta_ml,
                        consumo_atual_ml=0,
                        meta_alcancada=False,
                        id_user=usuario.id_user
                    )

                    db.add(meta)
                    db.commit()
                    db.refresh(meta) 
                    return meta
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
            detail=f"Erro inesperado ao criar meta para o usuário: {str(e)}")

def put_consumo_diario(db: Session, id_user: int, ml_consumida: int):
    try:
        if ml_consumida <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A quantidade a adicionar deve ser maior que zero.")
        
        meta_do_dia = get_meta_by_id(db, id_user)

        if meta_do_dia.consumo_atual_ml is None:
            meta_do_dia.consumo_atual_ml = 0

        meta_do_dia.consumo_atual_ml += ml_consumida
        meta_do_dia.meta_ml -= ml_consumida
        atualizar_meta_diaria = int(meta_do_dia.meta_ml)

        if atualizar_meta_diaria <= 0:
            meta_do_dia.meta_ml = 0
            meta_do_dia.meta_alcancada = True
        else:
            meta_do_dia.meta_alcancada = False


        db.commit()
        db.refresh(meta_do_dia)
        return meta_do_dia
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar consumo: {str(e)}")
  
def delete_metas(db: Session):
    try:
        deletados = db.query(MetaDiaria).delete()
        db.commit()
        return {"message": f"{deletados} Metas foram removidas com sucesso"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar usuários {str(e)}")
    
def delete_meta_by_id(db: Session, id_user: int):
    try:
        usuario = db.query(MetaDiaria).filter(MetaDiaria.id_user == id_user).first()
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        db.delete(usuario)
        db.commit()
        return {"message": f"Meta do usuário {id_user} removida com sucesso!"}
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=('Erro ao detelar meta'))