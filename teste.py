import sys
from PySide6.QtWidgets import QApplication
from app.ui.documentos.documentos_window import TodosDocumentosWindow

app = QApplication(sys.argv)
janela = TodosDocumentosWindow()
janela.show()
sys.exit(app.exec())