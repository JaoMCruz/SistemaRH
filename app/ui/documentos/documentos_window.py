import os

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QLineEdit
)
from PySide6.QtCore import Qt

from app.services.documento_service import DocumentoService
from app.services.funcionario_service import FuncionarioService

class TodosDocumentosWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.documento_service = DocumentoService()
        self.funcionario_service = FuncionarioService()

        self.setWindowTitle("Documentos")
        self.setGeometry(100, 100, 900, 500)

        layout = QVBoxLayout()

        titulo = QLabel("Documentos")
        titulo.setStyleSheet("font-size: 22px; font-weight: bold; color: #1E2761;")
        layout.addWidget(titulo)

        self.campo_busca = QLineEdit()
        self.campo_busca.setPlaceholderText("Buscar por nome do funcionário ou documento...")
        self.campo_busca.textChanged.connect(self.filtrar_documentos)
        layout.addWidget(self.campo_busca)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(3)
        self.tabela.setHorizontalHeaderLabels(["Funcionário", "Documento", "Enviado em"])
        layout.addWidget(self.tabela)

        botao_abrir = QPushButton("Abrir Selecionado")
        botao_abrir.clicked.connect(self.abrir_documento)
        layout.addWidget(botao_abrir)

        botao_excluir = QPushButton("Excluir Selecionado")
        botao_excluir.clicked.connect(self.excluir_documento)
        layout.addWidget(botao_excluir)

        self.setLayout(layout)
        self.carregar_documentos()

    def carregar_documentos(self):
        self.documentos = self.documento_service.listar_todos()
        self.exibir_documentos(self.documentos)

    def exibir_documentos(self, documentos):
        self.tabela.setRowCount(len(documentos))

        for linha, documento in enumerate(documentos):
            funcionario = self.funcionario_service.buscar_por_id(documento.funcionario_id)
            nome_funcionario = funcionario.nome if funcionario else "Desconhecido"

            item_funcionario = QTableWidgetItem(nome_funcionario)
            item_funcionario.setData(Qt.UserRole, documento.id)

            self.tabela.setItem(linha, 0, item_funcionario)
            self.tabela.setItem(linha, 1, QTableWidgetItem(documento.nome_arquivo))
            self.tabela.setItem(linha, 2, QTableWidgetItem(str(documento.enviado_em)))

    def filtrar_documentos(self, texto):
        texto = texto.lower()

        documentos_filtrados = []
        for documento in self.documentos:
            funcionario = self.funcionario_service.buscar_por_id(documento.funcionario_id)
            nome_funcionario = funcionario.nome if funcionario else ""

            if texto in nome_funcionario.lower() or texto in documento.nome_arquivo.lower():
                documentos_filtrados.append(documento)

        self.exibir_documentos(documentos_filtrados)

    def abrir_documento(self):
        linha_selecionada = self.tabela.currentRow()

        if linha_selecionada == -1:
            return

        item = self.tabela.item(linha_selecionada, 0)
        documento_id = item.data(Qt.UserRole)

        documento = self.documento_service.buscar_por_id(documento_id)
        os.startfile(documento.caminho_arquivo)

    def excluir_documento(self):
        linha_selecionada = self.tabela.currentRow()

        if linha_selecionada == -1:
            return

        item = self.tabela.item(linha_selecionada, 0)
        documento_id = item.data(Qt.UserRole)

        self.documento_service.excluir(documento_id)
        self.carregar_documentos()