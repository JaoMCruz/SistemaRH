from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
)
from PySide6.QtCore import Qt
from app.ui.funcionarios.funcionarios_window import FuncionariosWindow
from app.ui.documentos.documentos_window import TodosDocumentosWindow
from app.ui.funcionarios.funcionarios_window import CadastroFuncionarioWindow
from app.services.funcionario_service import FuncionarioService


class DashboardWindow(QWidget):
    def __init__(self, nome_usuario):
        super().__init__()
        self.setWindowTitle("Dashboard - Sistema de RH")
        self.setGeometry(100, 100, 1100, 650)

        layout_principal = QHBoxLayout()

        # ---- Menu lateral ----
        menu = QFrame()
        menu.setFixedWidth(220)
        menu.setStyleSheet("background-color: #2E7DE1;")

        layout_menu = QVBoxLayout()
        logo = QLabel("RH\nGestão de Pessoas")
        logo.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout_menu.addWidget(logo)
        layout_menu.addSpacing(20)

        botoes_menu = ["Início", "Funcionários", "Novo Funcionário", "Documentos", "Sair"]
        for texto in botoes_menu:
            botao = QPushButton(texto)
            botao.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: white;
                    text-align: left;
                    padding: 10px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #1B5FB8;
                }
            """)
            if texto == "Funcionários":
                botao.clicked.connect(self.abrir_funcionarios)

            if texto == "Novo Funcionário":
                botao.clicked.connect(self.abrir_novo_funcionario)

            if texto == "Documentos":
                botao.clicked.connect(self.abrir_documentos)

            layout_menu.addWidget(botao)

        layout_menu.addStretch()
        menu.setLayout(layout_menu)

        # ---- Área de conteúdo ----
        conteudo = QVBoxLayout()

        titulo = QLabel(f"Olá, {nome_usuario}!")
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #1E2761;")

        subtitulo = QLabel("Aqui está um resumo do seu sistema de RH.")
        subtitulo.setStyleSheet("font-size: 14px; color: #5A6B94;")

        conteudo.addWidget(titulo)
        conteudo.addWidget(subtitulo)
        conteudo.addSpacing(20)

        # ---- Cards ----
        linha_cards = QHBoxLayout()
        cards_info = [("Funcionários", "0"), ("Funcionários ativos", "0")]

        for label_texto, valor in cards_info:
            card = QFrame()
            card.setStyleSheet("background-color: white; border-radius: 8px; border: 1px solid #E0E4EE;")
            layout_card = QVBoxLayout()

            valor_label = QLabel(valor)
            valor_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #1E2761;")

            desc_label = QLabel(label_texto)
            desc_label.setStyleSheet("font-size: 13px; color: #5A6B94;")

            layout_card.addWidget(valor_label)
            layout_card.addWidget(desc_label)
            card.setLayout(layout_card)
            linha_cards.addWidget(card)

        conteudo.addLayout(linha_cards)
        conteudo.addStretch()

        layout_principal.addWidget(menu)
        layout_principal.addLayout(conteudo)

        self.setLayout(layout_principal)

    def abrir_funcionarios(self):
        self.janela_funcionarios = FuncionariosWindow()
        self.janela_funcionarios.show()

    def abrir_novo_funcionario(self):
        funcionario_service = FuncionarioService()
        self.janela_novo_funcionario = CadastroFuncionarioWindow(
        funcionario_service, lambda: None
    )
        self.janela_novo_funcionario.show()

    def abrir_documentos(self):
        self.janela_documentos = TodosDocumentosWindow()
        self.janela_documentos.show()