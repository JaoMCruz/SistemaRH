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
        self.repository.cadastrar(funcionario)

    def excluir(self, funcionario_id):
        self.repository.excluir(funcionario_id)

    def  atualizar(self, funcionario_id, dados):
        self.repository.atualizar(funcionario_id, dados)

    def buscar_por_id(self, funcionario_id):
        return self.repository.buscar_por_id(funcionario_id)