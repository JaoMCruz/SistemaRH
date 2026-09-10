import sys
from PySide6.QtWidgets import QApplication
from app.ui.boas_vindas.boas_vindas_window import BoasVindasWindow

app = QApplication(sys.argv)
janela = BoasVindasWindow()
janela.show()
sys.exit(app.exec())