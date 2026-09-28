from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, QSettings

from app.services.usuario_service import UsuarioService


class LoginWindow(QWidget):
    def __init__(self, callback_login_sucesso=None):
        super().__init__()
        self.callback_login_sucesso = callback_login_sucesso
        self.usuario_service = UsuarioService()

        layout = QVBoxLayout()
        layout.addStretch()

        card = QFrame()
        card.setFixedWidth(420)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 16px;
            }
        """)

        layout_card = QVBoxLayout()
        layout_card.setContentsMargins(40, 40, 40, 40)
        layout_card.setSpacing(15)

        titulo = QLabel("Entrar")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)
        layout_card.addWidget(titulo)

        self.campo_email = QLineEdit()
        self.campo_email.setPlaceholderText("E-mail")
        layout_card.addWidget(self.campo_email)

        self.campo_senha = QLineEdit()
        self.campo_senha.setPlaceholderText("Senha")
        self.campo_senha.setEchoMode(QLineEdit.Password)
        layout_card.addWidget(self.campo_senha)

        self.checkbox_lembrar = QCheckBox("Lembrar-me")
        layout_card.addWidget(self.checkbox_lembrar)

        layout_card.addSpacing(10)

        botao_entrar = QPushButton("Entrar")
        botao_entrar.clicked.connect(self.fazer_login)
        layout_card.addWidget(botao_entrar)

        card.setLayout(layout_card)

        layout.addWidget(card, alignment=Qt.AlignHCenter)
        layout.addStretch()
        self.setLayout(layout)

    def limpar_campos(self):
        self.campo_email.clear()
        self.campo_senha.clear()
        self.checkbox_lembrar.setChecked(False)

    def fazer_login(self):
        email = self.campo_email.text().strip()
        senha = self.campo_senha.text().strip()

        if not email or not senha:
            QMessageBox.warning(self, "Campos obrigatórios", "Preencha e-mail e senha.")
            return

        usuario = self.usuario_service.autenticar(email, senha)
        if usuario is None:
            QMessageBox.warning(self, "Erro", "E-mail ou senha inválidos.")
            return

        if self.checkbox_lembrar.isChecked():
            settings = QSettings("SistemaRH", "SistemaRH")
            settings.setValue("usuario_id", usuario.id)

        if self.callback_login_sucesso:
            self.callback_login_sucesso(usuario.nome)