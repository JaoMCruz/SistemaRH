from app.database.conexao import get_session
from app.models.funcionario import Funcionario


class FuncionarioRepository:
    def listar_todos(self):
        session = get_session()
        funcionarios = session.query(Funcionario).all()
        session.close()
        return funcionarios

    def cadastrar(self, funcionario):
        session = get_session()
        session.add(funcionario)
        session.commit()
        session.close()

    def buscar_por_id(self, funcionario_id):
        session = get_session()
        funcionario = session.query(Funcionario).filter(Funcionario.id == funcionario_id).first()
        session.close()
        return funcionario

    def excluir(self, funcionario_id):
        session = get_session()
        funcionario = session.query(Funcionario).filter(Funcionario.id == funcionario_id).first()
        session.delete(funcionario)
        session.commit()
        session.close()