from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP, Time
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.conexao import Base

class Usuarios(Base):
    __tablename__ = "usuario" 

    id_user = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=True)
    email = Column(String(255))
    senha = Column(String(255))
    idade = Column(Integer)
    peso = Column(Numeric(5,2))
    horario_dormir = Column(Time)
    horario_acordar = Column(Time)
    capacidade_garrafa_ml = Column(Integer)
    criado_em = Column(TIMESTAMP(timezone=True), server_default=func.now())
    meta = relationship("MetaDiaria", back_populates="usuario")