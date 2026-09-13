from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QLineEdit, QDateEdit, QListWidget, QFileDialog,
    QListWidgetItem, QMessageBox
)
from app.services.funcionario_service import FuncionarioService
from app.services.documento_service import DocumentoService
from PySide6.QtCore import QDate, Qt

import os


class FuncionariosWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.funcionario_service = FuncionarioService()

        self.setWindowTitle("Funcionários")
        self.setGeometry(100, 100, 900, 500)

        layout = QVBoxLayout()

        titulo = QLabel("Funcionários")
        titulo.setStyleSheet("font-size: 22px; font-weight: bold; color: #1E2761;")
        layout.addWidget(titulo)

        botao_novo = QPushButton("Novo Funcionário")
        botao_novo.clicked.connect(self.abrir_cadastro)
        layout.addWidget(botao_novo)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels(["Nome", "CPF", "Cargo", "Departamento", "Salário"])
        layout.addWidget(self.tabela)

        botao_excluir = QPushButton("Excluir Selecionado")
        botao_excluir.clicked.connect(self.excluir_funcionario)
        layout.addWidget(botao_excluir)

        botao_editar = QPushButton("Editar Selecionado")
        botao_editar.clicked.connect(self.editar_funcionario)
        layout.addWidget(botao_editar)

        botao_documentos = QPushButton("Documentos do Selecionado")
        botao_documentos.clicked.connect(self.abrir_documentos)
        layout.addWidget(botao_documentos)

        self.setLayout(layout)
        self.carregar_funcionarios()

    def excluir_funcionario(self):
        linha_selecionada = self.tabela.currentRow()

        if linha_selecionada == -1:
            return

        item = self.tabela.item(linha_selecionada, 0)
        funcionario_id = item.data(Qt.UserRole)
        nome_funcionario = item.text()

        resposta = QMessageBox.question(
            self,
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o funcionário '{nome_funcionario}'?",
        )

        if resposta == QMessageBox.Yes:
            self.funcionario_service.excluir(funcionario_id)
            self.carregar_funcionarios()

    def editar_funcionario(self):
        linha_selecionada = self.tabela.currentRow()

        if linha_selecionada == -1:
            return

        item = self.tabela.item(linha_selecionada, 0)
        funcionario_id = item.data(Qt.UserRole)

        funcionario = self.funcionario_service.buscar_por_id(funcionario_id)

        self.janela_editar = EditarFuncionarioWindow(
            self.funcionario_service, funcionario, self.carregar_funcionarios
        )
        self.janela_editar.show()

    def carregar_funcionarios(self):
        funcionarios = self.funcionario_service.listar_todos()

        self.tabela.setRowCount(len(funcionarios))

        for linha, funcionario in enumerate(funcionarios):

            item_nome = QTableWidgetItem(funcionario.nome)
            item_nome.setData(Qt.UserRole, funcionario.id)

            self.tabela.setItem(linha, 0, item_nome)
            self.tabela.setItem(linha, 1, QTableWidgetItem(funcionario.cpf))
            self.tabela.setItem(linha, 2, QTableWidgetItem(funcionario.cargo))
            self.tabela.setItem(linha, 3, QTableWidgetItem(funcionario.departamento))
            self.tabela.setItem(linha, 4, QTableWidgetItem(str(funcionario.salario)))

    def abrir_cadastro(self):
        self.janela_cadastro = CadastroFuncionarioWindow(
            self.funcionario_service, self.carregar_funcionarios
        )
        self.janela_cadastro.show()

    def abrir_documentos(self):
        linha_selecionada = self.tabela.currentRow()

        if linha_selecionada == -1:
            return

        item = self.tabela.item(linha_selecionada, 0)
        funcionario_id = item.data(Qt.UserRole)

        self.janela_documentos = DocumentosWindow(funcionario_id)
        self.janela_documentos.show()


class CadastroFuncionarioWindow(QWidget):
    def __init__(self, funcionario_service, callback_atualizar):
        super().__init__()
        self.funcionario_service = funcionario_service
        self.callback_atualizar = callback_atualizar

        self.setWindowTitle("Novo Funcionário")
        self.setGeometry(150, 150, 400, 400)

        layout = QVBoxLayout()

        self.campo_nome = QLineEdit()
        self.campo_nome.setPlaceholderText("Nome completo")

        self.campo_cpf = QLineEdit()
        self.campo_cpf.setPlaceholderText("CPF")

        self.campo_cargo = QLineEdit()
        self.campo_cargo.setPlaceholderText("Cargo")

        self.campo_departamento = QLineEdit()
        self.campo_departamento.setPlaceholderText("Departamento")

        self.campo_salario = QLineEdit()
        self.campo_salario.setPlaceholderText("Salário")

        self.campo_data_nascimento = QDateEdit()
        self.campo_data_nascimento.setCalendarPopup(True)
        self.campo_data_nascimento.setDate(QDate.currentDate())

        self.campo_data_admissao = QDateEdit()
        self.campo_data_admissao.setCalendarPopup(True)
        self.campo_data_admissao.setDate(QDate.currentDate())

        botao_salvar = QPushButton("Salvar")
        botao_salvar.clicked.connect(self.salvar)

        layout.addWidget(QLabel("Nome:"))
        layout.addWidget(self.campo_nome)
        layout.addWidget(QLabel("CPF:"))
        layout.addWidget(self.campo_cpf)
        layout.addWidget(QLabel("Cargo:"))
        layout.addWidget(self.campo_cargo)
        layout.addWidget(QLabel("Departamento:"))
        layout.addWidget(self.campo_departamento)
        layout.addWidget(QLabel("Salário:"))
        layout.addWidget(self.campo_salario)
        layout.addWidget(QLabel("Data de nascimento:"))
        layout.addWidget(self.campo_data_nascimento)
        layout.addWidget(QLabel("Data de admissão:"))
        layout.addWidget(self.campo_data_admissao)
        layout.addWidget(botao_salvar)

        self.setLayout(layout)

    def salvar(self):
        nome = self.campo_nome.text()
        cpf = self.campo_cpf.text()
        cargo = self.campo_cargo.text()
        departamento = self.campo_departamento.text()

        if not nome or not cpf or not cargo or not departamento:
            QMessageBox.warning(self, "Campos obrigatórios", "Preencha todos os campos antes de salvar.")
            return
    
        salario = float(self.campo_salario.text())

        data_nascimento = self.campo_data_nascimento.date().toPython()
        data_admissao = self.campo_data_admissao.date().toPython()

        self.funcionario_service.cadastrar(
            nome, cpf, data_nascimento, cargo, departamento, data_admissao, salario
        )

        self.callback_atualizar()
        self.close()


class EditarFuncionarioWindow(QWidget):
    def __init__(self, funcionario_service, funcionario, callback_atualizar):
        super().__init__()
        self.funcionario_service = funcionario_service
        self.funcionario = funcionario
        self.callback_atualizar = callback_atualizar

        self.setWindowTitle("Editar Funcionário")
        self.setGeometry(150, 150, 400, 400)

        layout = QVBoxLayout()

        self.campo_nome = QLineEdit(funcionario.nome)
        self.campo_cpf = QLineEdit(funcionario.cpf)
        self.campo_cargo = QLineEdit(funcionario.cargo)
        self.campo_departamento = QLineEdit(funcionario.departamento)
        self.campo_salario = QLineEdit(str(funcionario.salario))

        self.campo_data_nascimento = QDateEdit()
        self.campo_data_nascimento.setCalendarPopup(True)
        self.campo_data_nascimento.setDate(funcionario.data_nascimento)

        self.campo_data_admissao = QDateEdit()
        self.campo_data_admissao.setCalendarPopup(True)
        self.campo_data_admissao.setDate(funcionario.data_admissao)

        botao_salvar = QPushButton("Salvar Alterações")
        botao_salvar.clicked.connect(self.salvar)

        layout.addWidget(QLabel("Nome:"))
        layout.addWidget(self.campo_nome)
        layout.addWidget(QLabel("CPF:"))
        layout.addWidget(self.campo_cpf)
        layout.addWidget(QLabel("Cargo:"))
        layout.addWidget(self.campo_cargo)
        layout.addWidget(QLabel("Departamento:"))
        layout.addWidget(self.campo_departamento)
        layout.addWidget(QLabel("Salário:"))
        layout.addWidget(self.campo_salario)
        layout.addWidget(QLabel("Data de nascimento:"))
        layout.addWidget(self.campo_data_nascimento)
        layout.addWidget(QLabel("Data de admissão:"))
        layout.addWidget(self.campo_data_admissao)
        layout.addWidget(botao_salvar)

        self.setLayout(layout)

    def salvar(self):
        dados = {
            "nome": self.campo_nome.text(),
            "cpf": self.campo_cpf.text(),
            "cargo": self.campo_cargo.text(),
            "departamento": self.campo_departamento.text(),
            "salario": float(self.campo_salario.text()),
            "data_nascimento": self.campo_data_nascimento.date().toPython(),
            "data_admissao": self.campo_data_admissao.date().toPython(),
        }

        self.funcionario_service.atualizar(self.funcionario.id, dados)

        self.callback_atualizar()
        self.close()


class DocumentosWindow(QWidget):
    def __init__(self, funcionario_id):
        super().__init__()
        self.funcionario_id = funcionario_id
        self.documento_service = DocumentoService()

        self.setWindowTitle("Documentos do Funcionário")
        self.setGeometry(150, 150, 500, 400)

        layout = QVBoxLayout()

        titulo = QLabel("Documentos")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #1E2761;")
        layout.addWidget(titulo)

        botao_upload = QPushButton("Enviar Documento")
        botao_upload.clicked.connect(self.enviar_documento)
        layout.addWidget(botao_upload)

        self.lista_documentos = QListWidget()
        layout.addWidget(self.lista_documentos)

        self.lista_documentos.itemDoubleClicked.connect(self.abrir_documento)

        self.setLayout(layout)
        self.carregar_documentos()

    def carregar_documentos(self):
        self.lista_documentos.clear()
        documentos = self.documento_service.listar_por_funcionario(self.funcionario_id)

        for documento in documentos:
         item = QListWidgetItem(documento.nome_arquivo)
         item.setData(Qt.UserRole, documento.caminho_arquivo)
         self.lista_documentos.addItem(item)

    def enviar_documento(self):
        caminho, _ = QFileDialog.getOpenFileName(self, "Selecionar documento")

        if not caminho:
            return

        self.documento_service.cadastrar(self.funcionario_id, caminho)
        self.carregar_documentos()

    def abrir_documento(self, item):
        caminho = item.data(Qt.UserRole)
        os.startfile(caminho)