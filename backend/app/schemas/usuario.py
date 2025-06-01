from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date, time
from decimal import Decimal

class UsuarioBase(BaseModel):
    nome: str | None = None
    senha: str = Field(..., min_length=8, max_length=60)
    idade: int | None = None
    @field_validator('idade')
    @classmethod
    def validar_idade(cls, v):
        if v is not None:
            if v < 5:
                raise ValueError("Idade mínima: 5 anos")
            elif v > 120:
                raise ValueError("Idade máxima: 120 anos")
        return v
    peso: float | None = None
    @field_validator('peso')
    @classmethod
    def validar_peso(cls, v):
        if v is not None:
            if isinstance(v, Decimal):
                v = float(v)
            elif v <= 5:
                raise ValueError("Peso mínimo: 5kg")
            elif v > 300:
                raise ValueError("Peso máximo: 300kg")
        return v
    horario_dormir: time
    horario_acordar: time
    capacidade_garrafa_ml: int

    class Config:
        from_attributes = True 

class UsuarioResponse(UsuarioBase):
    nome: str
    criado_em: date

    class Config:
        from_attributes = True