import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QMessageBox, QDateEdit, QHeaderView,
    QListWidget, QListWidgetItem, QFileDialog
)
from PySide6.QtCore import Qt, QDate
from sqlalchemy.exc import IntegrityError


class FuncionariosWindow(QWidget):
    def __init__(self, callback_abrir_cadastro=None, callback_abrir_editar=None, callback_abrir_documentos=None):
        super().__init__()
        from app.services.funcionario_service import FuncionarioService
        from app.services.documento_service import DocumentoService

        self.funcionario_service = FuncionarioService()
        self.documento_service = DocumentoService()

        self.callback_abrir_cadastro = callback_abrir_cadastro
        self.callback_abrir_editar = callback_abrir_editar
        self.callback_abrir_documentos = callback_abrir_documentos

        self.funcionarios_atuais = []

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)

        titulo = QLabel("Funcionários")
        titulo.setObjectName("titulo")
        layout.addWidget(titulo)

        linha_topo = QHBoxLayout()
        self.campo_busca = QLineEdit()
        self.campo_busca.setPlaceholderText("Buscar por nome ou CPF...")
        self.campo_busca.textChanged.connect(self.filtrar_funcionarios)

        botao_novo = QPushButton("Novo Funcionário")
        botao_novo.clicked.connect(self.abrir_cadastro)

        linha_topo.addWidget(self.campo_busca)
        linha_topo.addWidget(botao_novo)
        layout.addLayout(linha_topo)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels(["Nome", "CPF", "Cargo", "Departamento", "Salário"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.tabela)

        linha_botoes = QHBoxLayout()
        botao_editar = QPushButton("Editar")
        botao_documentos = QPushButton("Documentos")
        botao_excluir = QPushButton("Excluir")

        botao_editar.clicked.connect(self.editar_funcionario)
        botao_documentos.clicked.connect(self.abrir_documentos)
        botao_excluir.clicked.connect(self.excluir_funcionario)

        linha_botoes.addWidget(botao_editar)
        linha_botoes.addWidget(botao_documentos)
        linha_botoes.addWidget(botao_excluir)
        layout.addLayout(linha_botoes)

        self.setLayout(layout)
        self.carregar_funcionarios()

    def carregar_funcionarios(self):
        self.funcionarios_atuais = self.funcionario_service.listar_todos()
        self.exibir_funcionarios(self.funcionarios_atuais)

    def exibir_funcionarios(self, funcionarios):
        self.tabela.setRowCount(0)
        for funcionario in funcionarios:
            linha = self.tabela.rowCount()
            self.tabela.insertRow(linha)

            item_nome = QTableWidgetItem(funcionario.nome)
            item_nome.setData(Qt.UserRole, funcionario.id)

            self.tabela.setItem(linha, 0, item_nome)
            self.tabela.setItem(linha, 1, QTableWidgetItem(funcionario.cpf))
            self.tabela.setItem(linha, 2, QTableWidgetItem(funcionario.cargo))
            self.tabela.setItem(linha, 3, QTableWidgetItem(funcionario.departamento))
            self.tabela.setItem(linha, 4, QTableWidgetItem(f"R$ {funcionario.salario:.2f}"))

    def filtrar_funcionarios(self, texto):
        texto = texto.lower().strip()
        if not texto:
            self.exibir_funcionarios(self.funcionarios_atuais)
            return
        filtrados = [
            f for f in self.funcionarios_atuais
            if texto in f.nome.lower() or texto in f.cpf.lower()
        ]
        self.exibir_funcionarios(filtrados)

    def _funcionario_selecionado_id(self):
        linha = self.tabela.currentRow()
        if linha == -1:
            QMessageBox.warning(self, "Atenção", "Selecione um funcionário na tabela.")
            return None
        item = self.tabela.item(linha, 0)
        return item.data(Qt.UserRole)

    def abrir_cadastro(self):
        if self.callback_abrir_cadastro:
            self.callback_abrir_cadastro()

    def editar_funcionario(self):
        funcionario_id = self._funcionario_selecionado_id()
        if funcionario_id is None:
            return
        if self.callback_abrir_editar:
            self.callback_abrir_editar(funcionario_id)

    def abrir_documentos(self):
        funcionario_id = self._funcionario_selecionado_id()
        if funcionario_id is None:
            return
        if self.callback_abrir_documentos:
            self.callback_abrir_documentos(funcionario_id)

    def excluir_funcionario(self):
        funcionario_id = self._funcionario_selecionado_id()
        if funcionario_id is None:
            return

        total_documentos = self.documento_service.contar_por_funcionario(funcionario_id)
        if total_documentos > 0:
            QMessageBox.warning(
                self, "Não é possível excluir",
                "Este funcionário possui documentos vinculados. Exclua os documentos antes de excluir o funcionário."
            )
            return

        resposta = QMessageBox.question(
            self, "Confirmar exclusão",
            "Tem certeza que deseja excluir este funcionário?",
            QMessageBox.Yes | QMessageBox.No
        )
        if resposta == QMessageBox.Yes:
            self.funcionario_service.excluir(funcionario_id)
            self.carregar_funcionarios()


class CadastroFuncionarioWindow(QWidget):
    def __init__(self, funcionario_service, callback_atualizar):
        super().__init__()
        self.funcionario_service = funcionario_service
        self.callback_atualizar = callback_atualizar

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)

        titulo = QLabel("Novo Funcionário")
        titulo.setObjectName("titulo")
        layout.addWidget(titulo)

        self.campo_nome = QLineEdit()
        self.campo_nome.setPlaceholderText("Nome completo")

        self.campo_cpf = QLineEdit()
        self.campo_cpf.setPlaceholderText("CPF")

        self.campo_data_nascimento = QDateEdit()
        self.campo_data_nascimento.setCalendarPopup(True)
        self.campo_data_nascimento.setDate(QDate.currentDate())

        self.campo_cargo = QLineEdit()
        self.campo_cargo.setPlaceholderText("Cargo")

        self.campo_departamento = QLineEdit()
        self.campo_departamento.setPlaceholderText("Departamento")

        self.campo_data_admissao = QDateEdit()
        self.campo_data_admissao.setCalendarPopup(True)
        self.campo_data_admissao.setDate(QDate.currentDate())

        self.campo_salario = QLineEdit()
        self.campo_salario.setPlaceholderText("Salário (ex: 2500.00)")

        for texto, campo in [
            ("Nome", self.campo_nome), ("CPF", self.campo_cpf),
            ("Data de nascimento", self.campo_data_nascimento),
            ("Cargo", self.campo_cargo), ("Departamento", self.campo_departamento),
            ("Data de admissão", self.campo_data_admissao),
            ("Salário", self.campo_salario),
        ]:
            layout.addWidget(QLabel(texto))
            layout.addWidget(campo)

        linha_botoes = QHBoxLayout()
        botao_salvar = QPushButton("Salvar")
        botao_salvar.clicked.connect(self.salvar)

        botao_cancelar = QPushButton("Cancelar")
        botao_cancelar.setStyleSheet("background-color: #AAAAAA;")
        botao_cancelar.clicked.connect(self.callback_atualizar)

        linha_botoes.addWidget(botao_salvar)
        linha_botoes.addWidget(botao_cancelar)
        layout.addLayout(linha_botoes)

        layout.addStretch()
        self.setLayout(layout)

    def salvar(self):
        nome = self.campo_nome.text().strip()
        cpf = self.campo_cpf.text().strip()
        cargo = self.campo_cargo.text().strip()
        departamento = self.campo_departamento.text().strip()
        salario_texto = self.campo_salario.text().strip()

        if not nome or not cpf or not cargo or not departamento or not salario_texto:
            QMessageBox.warning(self, "Campos obrigatórios", "Preencha todos os campos.")
            return

        try:
            salario = float(salario_texto.replace(",", "."))
        except ValueError:
            QMessageBox.warning(self, "Salário inválido", "Digite um valor numérico válido para o salário.")
            return

        try:
            self.funcionario_service.cadastrar(
                nome=nome,
                cpf=cpf,
                data_nascimento=self.campo_data_nascimento.date().toPython(),
                cargo=cargo,
                departamento=departamento,
                data_admissao=self.campo_data_admissao.date().toPython(),
                salario=salario
            )
        except IntegrityError:
            QMessageBox.warning(self, "CPF duplicado", "Já existe um funcionário cadastrado com esse CPF.")
            return

        QMessageBox.information(self, "Sucesso", "Funcionário cadastrado com sucesso!")
        self.callback_atualizar()


class EditarFuncionarioWindow(QWidget):
    def __init__(self, funcionario_service, funcionario_id, callback_atualizar):
        super().__init__()
        self.funcionario_service = funcionario_service
        self.funcionario_id = funcionario_id
        self.callback_atualizar = callback_atualizar

        funcionario = self.funcionario_service.buscar_por_id(funcionario_id)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)

        titulo = QLabel("Editar Funcionário")
        titulo.setObjectName("titulo")
        layout.addWidget(titulo)

        self.campo_nome = QLineEdit(funcionario.nome)
        self.campo_cpf = QLineEdit(funcionario.cpf)

        self.campo_data_nascimento = QDateEdit()
        self.campo_data_nascimento.setCalendarPopup(True)
        self.campo_data_nascimento.setDate(QDate(
            funcionario.data_nascimento.year, funcionario.data_nascimento.month, funcionario.data_nascimento.day
        ))

        self.campo_cargo = QLineEdit(funcionario.cargo)
        self.campo_departamento = QLineEdit(funcionario.departamento)

        self.campo_data_admissao = QDateEdit()
        self.campo_data_admissao.setCalendarPopup(True)
        self.campo_data_admissao.setDate(QDate(
            funcionario.data_admissao.year, funcionario.data_admissao.month, funcionario.data_admissao.day
        ))

        self.campo_salario = QLineEdit(str(funcionario.salario))

        for texto, campo in [
            ("Nome", self.campo_nome), ("CPF", self.campo_cpf),
            ("Data de nascimento", self.campo_data_nascimento),
            ("Cargo", self.campo_cargo), ("Departamento", self.campo_departamento),
            ("Data de admissão", self.campo_data_admissao),
            ("Salário", self.campo_salario),
        ]:
            layout.addWidget(QLabel(texto))
            layout.addWidget(campo)

        linha_botoes = QHBoxLayout()
        botao_salvar = QPushButton("Salvar alterações")
        botao_salvar.clicked.connect(self.salvar)

        botao_cancelar = QPushButton("Cancelar")
        botao_cancelar.setStyleSheet("background-color: #AAAAAA;")
        botao_cancelar.clicked.connect(self.callback_atualizar)

        linha_botoes.addWidget(botao_salvar)
        linha_botoes.addWidget(botao_cancelar)
        layout.addLayout(linha_botoes)

        layout.addStretch()
        self.setLayout(layout)

    def salvar(self):
        nome = self.campo_nome.text().strip()
        cpf = self.campo_cpf.text().strip()
        cargo = self.campo_cargo.text().strip()
        departamento = self.campo_departamento.text().strip()
        salario_texto = self.campo_salario.text().strip()

        if not nome or not cpf or not cargo or not departamento or not salario_texto:
            QMessageBox.warning(self, "Campos obrigatórios", "Preencha todos os campos.")
            return

        try:
            salario = float(salario_texto.replace(",", "."))
        except ValueError:
            QMessageBox.warning(self, "Salário inválido", "Digite um valor numérico válido para o salário.")
            return

        dados = {
            "nome": nome,
            "cpf": cpf,
            "cargo": cargo,
            "departamento": departamento,
            "data_nascimento": self.campo_data_nascimento.date().toPython(),
            "data_admissao": self.campo_data_admissao.date().toPython(),
            "salario": salario,
        }

        try:
            self.funcionario_service.atualizar(self.funcionario_id, dados)
        except IntegrityError:
            QMessageBox.warning(self, "CPF duplicado", "Já existe outro funcionário cadastrado com esse CPF.")
            return

        QMessageBox.information(self, "Sucesso", "Funcionário atualizado com sucesso!")
        self.callback_atualizar()


class DocumentosFuncionarioWindow(QWidget):
    def __init__(self, documento_service, funcionario_service, funcionario_id, callback_voltar):
        super().__init__()
        self.documento_service = documento_service
        self.funcionario_id = funcionario_id
        self.callback_voltar = callback_voltar

        funcionario = funcionario_service.buscar_por_id(funcionario_id)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)

        titulo = QLabel(f"Documentos de {funcionario.nome}")
        titulo.setObjectName("titulo")
        layout.addWidget(titulo)

        linha_topo = QHBoxLayout()
        botao_enviar = QPushButton("Enviar documento")
        botao_enviar.clicked.connect(self.enviar_documento)
        botao_voltar = QPushButton("Voltar para Funcionários")
        botao_voltar.setStyleSheet("background-color: #AAAAAA;")
        botao_voltar.clicked.connect(lambda: self.callback_voltar())
        linha_topo.addWidget(botao_enviar)
        linha_topo.addWidget(botao_voltar)
        layout.addLayout(linha_topo)

        self.lista = QListWidget()
        self.lista.itemDoubleClicked.connect(self.abrir_documento)
        layout.addWidget(self.lista)

        botao_excluir = QPushButton("Excluir documento selecionado")
        botao_excluir.clicked.connect(self.excluir_documento)
        layout.addWidget(botao_excluir)

        self.setLayout(layout)
        self.carregar_documentos()

    def carregar_documentos(self):
        self.lista.clear()
        documentos = self.documento_service.listar_por_funcionario(self.funcionario_id)
        for documento in documentos:
            item = QListWidgetItem(documento.nome_arquivo)
            item.setData(Qt.UserRole, documento.id)
            self.lista.addItem(item)

    def enviar_documento(self):
        caminho, _ = QFileDialog.getOpenFileName(self, "Selecionar documento")
        if caminho:
            self.documento_service.cadastrar(self.funcionario_id, caminho)
            self.carregar_documentos()

    def abrir_documento(self, item):
        documento_id = item.data(Qt.UserRole)
        documento = self.documento_service.buscar_por_id(documento_id)
        os.startfile(documento.caminho_arquivo)

    def excluir_documento(self):
        item = self.lista.currentItem()
        if not item:
            QMessageBox.warning(self, "Atenção", "Selecione um documento na lista.")
            return
        resposta = QMessageBox.question(
            self, "Confirmar exclusão", "Deseja excluir este documento?",
            QMessageBox.Yes | QMessageBox.No
        )
        if resposta == QMessageBox.Yes:
            documento_id = item.data(Qt.UserRole)
            self.documento_service.excluir(documento_id)
            self.carregar_documentos()