# # backend/app/schemas/lembretes.py

# from pydantic import BaseModel, Field
# from datetime import datetime, date
# from typing import Optional

# class LembreteHidratacaoBase(BaseModel):
#     data_lembrete: date
#     horario_previsto: datetime
#     tipo_lembrete: str
#     status_interacao: bool = False
#     horario_interacao: Optional[datetime]
    
#     class Config:
#         from_attributes = True

# class LembreteResponse(LembreteHidratacaoBase):
#     id_lembrete: int
#     id_user: int
#     tipo_lembrete: str
#     status_interacao: str
#     data_lembrete: date
