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
        self.campo_usuario = QLineEdit()

        label_senha = QLabel("Senha:")
        self.campo_senha = QLineEdit()
        self.campo_senha.setEchoMode(QLineEdit.EchoMode.Password)

        botao_entrar = QPushButton("Entrar")

        layout.addWidget(label_usuario)
        layout.addWidget(self.campo_usuario)
        layout.addWidget(label_senha)
        layout.addWidget(self.campo_senha)
        layout.addWidget(botao_entrar)

        botao_entrar.clicked.connect(self.fazer_login)

        self.setLayout(layout)

    def fazer_login(self):
        email = self.campo_usuario.text()
        senha = self.campo_senha.text()

        usuario = self.usuario_service.autenticar(email, senha)

        if usuario:
           print(f"Login bem-sucedido! Bem-vindo, {usuario.nome}!")

        else:
            print("Falha no login. Usuário ou senha incorretos.")

        

            