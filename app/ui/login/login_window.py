from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from app.services.usuario_service import UsuarioService

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.usuario_service = UsuarioService()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 500, 300)

        layout = QVBoxLayout()
        label_usuario = QLabel("Usuário:")
        campo_usuario = QLineEdit()

        label_senha = QLabel("Senha:")
        campo_senha = QLineEdit()
        campo_senha.setEchoMode(QLineEdit.EchoMode.Password)

        botao_entrar = QPushButton("Entrar")

        layout.addWidget(label_usuario)
        layout.addWidget(campo_usuario)
        layout.addWidget(label_senha)
        layout.addWidget(campo_senha)
        layout.addWidget(botao_entrar)

        self.setLayout(layout)

    def fazer_login(self):
        email = campo_usuario.text()
        senha = campo_senha.text()

        usuario = self.usuario_service.autenticar(email, senha)

        if usuario:
            print("Email ou senhas invalidos!")

        else:
            print(f"Login bem-sucedido! Bem-vindo, {usuario.nome}!")

        

            