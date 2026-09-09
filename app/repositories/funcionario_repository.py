from app.database.conexao import get_session
from app.models import funcionario
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

    def atualizar(self, funcionario_id, dados):
        session = get_session()
        funcionario = session.query(Funcionario).filter(Funcionario.id == funcionario_id).first()

        funcionario.nome = dados['nome']
        funcionario.cpf = dados['cpf']
        funcionario.cargo = dados['cargo']
        funcionario.departamento = dados["departamento"]
        funcionario.data_nascimento = dados["data_nascimento"]
        funcionario.data_admissao = dados["data_admissao"]
        funcionario.salario = dados['salario']

        session.commit()
        session.close()