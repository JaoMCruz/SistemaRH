from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame
from PySide6.QtCore import Qt


class BoasVindasWindow(QWidget):
    def __init__(self, callback_entrar=None):
        super().__init__()
        self.callback_entrar = callback_entrar

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

        titulo = QLabel("Sistema de RH")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)

        subtitulo = QLabel("Gestão de funcionários simplificada")
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setStyleSheet("color: #888888; font-size: 13px;")

        botao_entrar = QPushButton("Entrar")
        botao_entrar.clicked.connect(self.abrir_login)

        layout_card.addWidget(titulo)
        layout_card.addWidget(subtitulo)
        layout_card.addSpacing(10)
        layout_card.addWidget(botao_entrar)
        card.setLayout(layout_card)

        layout.addWidget(card, alignment=Qt.AlignHCenter)
        layout.addStretch()
        self.setLayout(layout)

    def abrir_login(self):
        if self.callback_entrar:
            self.callback_entrar()