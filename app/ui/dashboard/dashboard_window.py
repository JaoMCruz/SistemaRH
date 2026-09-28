from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QStackedWidget
)
from PySide6.QtCore import Qt, QSettings

from app.ui.funcionarios.funcionarios_window import (
    FuncionariosWindow, CadastroFuncionarioWindow, EditarFuncionarioWindow, DocumentosFuncionarioWindow
)
from app.ui.documentos.documentos_window import TodosDocumentosWindow
from app.services.funcionario_service import FuncionarioService
from app.services.documento_service import DocumentoService


class DashboardWindow(QWidget):
    def __init__(self, nome_usuario, callback_sair=None):
        super().__init__()
        self.nome_usuario = nome_usuario
        self.callback_sair = callback_sair

        self.funcionario_service = FuncionarioService()
        self.documento_service = DocumentoService()

        layout_principal = QHBoxLayout()

        menu = QFrame()
        menu.setFixedWidth(200)
        menu.setStyleSheet("background-color: #2E7DE1;")
        layout_menu = QVBoxLayout()
        layout_menu.setContentsMargins(15, 30, 15, 30)
        layout_menu.setSpacing(10)

        titulo_menu = QLabel("Sistema RH")
        titulo_menu.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        layout_menu.addWidget(titulo_menu)
        layout_menu.addSpacing(20)

        estilo_botao_menu = """
            QPushButton {
                background-color: transparent;
                color: white;
                text-align: left;
                padding: 10px;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1E2761;
                border-radius: 6px;
            }
        """

        botao_inicio = QPushButton("Início")
        botao_funcionarios = QPushButton("Funcionários")
        botao_documentos = QPushButton("Documentos")
        botao_sair = QPushButton("Sair")

        for botao in (botao_inicio, botao_funcionarios, botao_documentos, botao_sair):
            botao.setStyleSheet(estilo_botao_menu)
            botao.setCursor(Qt.PointingHandCursor)
            layout_menu.addWidget(botao)

        layout_menu.addStretch()
        menu.setLayout(layout_menu)

        botao_inicio.clicked.connect(self.mostrar_inicio)
        botao_funcionarios.clicked.connect(self.mostrar_funcionarios)
        botao_documentos.clicked.connect(self.mostrar_documentos)
        botao_sair.clicked.connect(self.sair)

        self.pagina_inicio = QWidget()
        layout_inicio = QVBoxLayout()
        layout_inicio.setContentsMargins(30, 30, 30, 30)

        titulo_boas_vindas = QLabel(f"Olá, {self.nome_usuario}!")
        titulo_boas_vindas.setObjectName("titulo")
        layout_inicio.addWidget(titulo_boas_vindas)
        layout_inicio.addSpacing(20)

        layout_cards = QHBoxLayout()
        self.card_total_funcionarios = self.criar_card("Funcionários", "0")
        self.card_funcionarios_ativos = self.criar_card("Funcionários ativos", "0")
        layout_cards.addWidget(self.card_total_funcionarios)
        layout_cards.addWidget(self.card_funcionarios_ativos)
        layout_cards.addStretch()

        layout_inicio.addLayout(layout_cards)
        layout_inicio.addStretch()
        self.pagina_inicio.setLayout(layout_inicio)

        self.pagina_funcionarios = FuncionariosWindow(
            callback_abrir_cadastro=self.mostrar_cadastro,
            callback_abrir_editar=self.mostrar_editar,
            callback_abrir_documentos=self.mostrar_documentos_funcionario
        )

        self.pagina_documentos = TodosDocumentosWindow()

        self.pagina_formulario = QWidget()
        self.layout_formulario = QVBoxLayout()
        self.pagina_formulario.setLayout(self.layout_formulario)

        self.pagina_documentos_funcionario = QWidget()
        self.layout_documentos_funcionario = QVBoxLayout()
        self.pagina_documentos_funcionario.setLayout(self.layout_documentos_funcionario)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.pagina_inicio)
        self.stack.addWidget(self.pagina_funcionarios)
        self.stack.addWidget(self.pagina_documentos)
        self.stack.addWidget(self.pagina_formulario)
        self.stack.addWidget(self.pagina_documentos_funcionario)

        layout_principal.addWidget(menu)
        layout_principal.addWidget(self.stack)
        self.setLayout(layout_principal)

        self.atualizar_cards()

    def criar_card(self, titulo, valor):
        card = QFrame()
        card.setFixedSize(180, 100)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #ddd;
            }
        """)
        layout_card = QVBoxLayout()
        label_valor = QLabel(valor)
        label_valor.setStyleSheet("font-size: 26px; font-weight: bold; color: #2E7DE1;")
        label_titulo = QLabel(titulo)
        label_titulo.setStyleSheet("font-size: 12px; color: #555;")
        layout_card.addWidget(label_valor)
        layout_card.addWidget(label_titulo)
        card.setLayout(layout_card)
        card.label_valor = label_valor
        return card

    def atualizar_cards(self):
        total = len(self.funcionario_service.listar_todos())
        self.card_total_funcionarios.label_valor.setText(str(total))
        self.card_funcionarios_ativos.label_valor.setText(str(total))

    def _limpar_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def mostrar_inicio(self):
        self.atualizar_cards()
        self.stack.setCurrentWidget(self.pagina_inicio)

    def mostrar_funcionarios(self):
        self.pagina_funcionarios.carregar_funcionarios()
        self.stack.setCurrentWidget(self.pagina_funcionarios)

    def mostrar_documentos(self):
        self.pagina_documentos.carregar_documentos()
        self.stack.setCurrentWidget(self.pagina_documentos)

    def mostrar_cadastro(self):
        self._limpar_layout(self.layout_formulario)
        formulario = CadastroFuncionarioWindow(self.funcionario_service, self.voltar_para_funcionarios)
        self.layout_formulario.addWidget(formulario)
        self.stack.setCurrentWidget(self.pagina_formulario)

    def mostrar_editar(self, funcionario_id):
        self._limpar_layout(self.layout_formulario)
        formulario = EditarFuncionarioWindow(self.funcionario_service, funcionario_id, self.voltar_para_funcionarios)
        self.layout_formulario.addWidget(formulario)
        self.stack.setCurrentWidget(self.pagina_formulario)

    def mostrar_documentos_funcionario(self, funcionario_id):
        self._limpar_layout(self.layout_documentos_funcionario)
        pagina = DocumentosFuncionarioWindow(
            self.documento_service, self.funcionario_service, funcionario_id, self.mostrar_funcionarios
        )
        self.layout_documentos_funcionario.addWidget(pagina)
        self.stack.setCurrentWidget(self.pagina_documentos_funcionario)

    def voltar_para_funcionarios(self):
        self.mostrar_funcionarios()

    def sair(self):
        settings = QSettings("SistemaRH", "SistemaRH")
        settings.remove("usuario_id")
        if self.callback_sair:
            self.callback_sair()