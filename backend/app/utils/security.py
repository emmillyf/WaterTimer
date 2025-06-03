from passlib.context import CryptContext
from fastapi.security  import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models.usuario import Usuarios
from fastapi import Depends, status, HTTPException
from database.conexao import get_db
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from jwt import encode, decode, DecodeError
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = 'HS256'
EXPIRACAO_TOKEN = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login")

def get_senha_hash(senha:str):
    return pwd_context.hash(senha)

def verificar_senha(senha: str, hashed_senha: str):
    return pwd_context.verify(senha, hashed_senha)

def criar_acesso_token(data: dict):
    to_encode = data.copy()
    
    tempo_de_expiracao = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=EXPIRACAO_TOKEN
    )

    to_encode["exp"] = tempo_de_expiracao

    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user_atual(db: Session = Depends(get_db),
                token: str = Depends(oauth2_scheme)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credênciais",
        headers={'WWW-Authenticate': 'Bearer'},)
    try:
        payload = decode(token, SECRET_KEY, algorithms=ALGORITHM)
        subject_email = payload.get('sub')
        if not subject_email:
            raise credentials_exception
    except DecodeError:
        raise credentials_exception
    user = db.query(Usuarios).filter(Usuarios.email==subject_email).first()

    if not user:
        raise credentials_exception

    return user