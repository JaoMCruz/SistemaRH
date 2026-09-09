from app.repositories.funcionario_repository import FuncionarioRepository
from app.models.funcionario import Funcionario


class FuncionarioService:
    def __init__(self):
        self.repository = FuncionarioRepository()

    def listar_todos(self):
        return self.repository.listar_todos()

    def cadastrar(self, nome, cpf, data_nascimento, cargo, departamento, data_admissao, salario):
        funcionario = Funcionario(
            nome=nome,
            cpf=cpf,
            data_nascimento=data_nascimento,
            cargo=cargo,
            departamento=departamento,
            data_admissao=data_admissao,
            salario=salario
        )
        return self.repository.cadastrar(funcionario)