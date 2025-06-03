# from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Boolean
# from sqlalchemy.orm import relationship
# from datetime import date
# from database.conexao import Base

# class LembreteHidratacao(Base):
#     __tablename__ = "lembretes_hidratacao"
#     __table_args__ = {'extend_existing': True}

#     id_lembrete = Column(Integer, primary_key=True,  autoincrement=True)
#     id_user = Column(Integer, ForeignKey('usuario.id_user'), nullable=True)
#     id_meta = Column(Integer, ForeignKey("meta_diaria.id_meta", nullable=True))
#     data_lembrete = Column(Date, nullable=False, default=date.today) # A data específica do lembrete
#     horario_previsto = Column(DateTime, nullable=False) # Data e hora que o lembrete deveria disparar
#     tipo_lembrete = Column(String(50), nullable=False) # 'hidratacao_regular', 'garrafa_quase_vazia'
#     status_interacao = Column(String(20), nullable=False, default='pendente') # 'concluido', 'cancelado'
#     usuario = relationship("Usuarios", back_populates="lembrete")
#     meta = relationship("MetaDiaria", back_populates="lembrete")
    
