from pydantic import BaseModel, Field, field_validator, EmailStr
from datetime import date, time
from typing import Optional
import re
class UsuarioBase(BaseModel):
    nome: str | None = None
    email: EmailStr | None = Field(None, max_length=60)
    senha: str = Field(..., min_length=8, max_length=60)
    @field_validator('senha')
    @classmethod
    def validar_senha(cls, v):
        pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>_\-+=]).{8,60}$'

        if not re.match(pattern, v):
            raise ValueError(
                "A senha deve conter entre 8 e 60 caracteres, " \
                "incluindo ao menos uma letra maiúscula, um número e um caractere especial."
            )
        return v
    
    idade: int  = Field(None, ge=5, le=100, description="Idade mínima é de 5 anos e idade máxima é de 100")
    peso: float = Field(None, ge=5, le=300, description="Peso mínimo é de 5kg e peso máximo é de 300kg")
    horario_dormir: time
    horario_acordar: time
    capacidade_garrafa_ml: int = Field(None, ge=100, le=2000)
    
    class Config:
        from_attributes = True 

class UsuarioResponse(UsuarioBase):
    criado_em: date
    class Config:
        from_attributes = True

class UsuarioUpdate(UsuarioBase):
    nome: Optional[str] | None
    email: Optional[EmailStr] | None = Field(None, max_length=60)
    senha: Optional[str] | None
    idade: Optional[int]  = Field(None, ge=5, le=100, description="Idade mínima é de 5 anos e idade máxima é de 100")
    peso: Optional[float] = Field(None, ge=5, le=300, description="Peso mínimo é de 5kg e peso máximo é de 300kg")
    horario_acordar: Optional[time] | None
    horario_dormir: Optional[time] | None
    capacidade_garrafa_ml: Optional[int] | None
    criado_em: Optional[date] | None

class UsuarioMetaRequest(BaseModel):
    peso: float = Field(..., ge=5, le=300)
    idade: int = Field(..., ge=5, le=100)