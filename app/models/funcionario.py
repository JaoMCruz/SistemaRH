from sqlalchemy import Column, Integer, String, Date, Numeric
from app.database.conexao import Base

class Funcionario(Base):
    __tablename__ = 'funcionarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False) 
    data_nascimento = Column(Date, nullable=False)
    cargo = Column(String(100), nullable=False)
    departamento = Column(String(100), nullable=False)
    data_admissao = Column(Date, nullable=False)
    salario = Column(Numeric(10, 2), nullable=False)

    