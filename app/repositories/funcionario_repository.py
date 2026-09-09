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