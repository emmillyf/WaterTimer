from pydantic import BaseModel, Field
from datetime import date
from database.conexao import Base

class MetaDiaria(BaseModel):
    meta_ml: int
    consumo_atual_ml: int
    meta_alcancada: bool = False

    class Config:
        from_attributes = True

class MetaDiariaResponse(MetaDiaria):
    data: date

    class Config:
        from_attributes = True