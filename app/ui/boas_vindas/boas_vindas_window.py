from PySide6.QtWidgets import  QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from app.ui.login.login_window import LoginWindow

class BoasVindasWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bem-vindo")
        self.setGeometry(100, 100, 500, 300)

        layout = QVBoxLayout()
        titulo=QLabel("Bem-vindo ao Sistema de Recursos Humanos")
        botao=QPushButton("Iniciar")
        botao.clicked.connect(self.abrir_login)

        layout.addStretch()
        layout.addWidget(titulo, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(botao, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)

    def abrir_login(self):
            self.login_window = LoginWindow()
            self.login_window.show()
            self.close()
