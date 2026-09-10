from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database.conexao import Base

class Documento(Base):
    __tablename__ = 'documentos'

    id = Column(Integer, primary_key=True)
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=False)
    nome_arquivo = Column(String(255), nullable=False)
    caminho_arquivo = Column(String(500), nullable=False)
    enviado_em = Column(DateTime, server_default=func.now())