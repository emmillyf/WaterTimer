from sqlalchemy import Column, Integer, ForeignKey, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.conexao import Base

class MetaDiaria(Base):
    __tablename__ = "meta_diaria"
    __table_args__ = {'extend_existing': True}

    id_meta = Column(Integer, primary_key=True,  autoincrement=True)
    data = Column(TIMESTAMP(timezone=True), server_default=func.now())
    meta_ml = Column(Integer, default=0)
    consumo_atual_ml = Column(Integer)
    meta_alcancada = Column(Boolean)
    id_user = Column(Integer, ForeignKey('usuario.id_user'), nullable=True)
    usuario = relationship("Usuarios", back_populates="meta")

