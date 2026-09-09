import sys
from PySide6.QtWidgets import QApplication
from app.ui.funcionarios.funcionarios_window import FuncionariosWindow

app = QApplication(sys.argv)
janela = FuncionariosWindow()
janela.show()
sys.exit(app.exec())