import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSettings

from app.ui.estilo import ESTILO_GLOBAL
from app.ui.main_window import MainWindow
from app.services.usuario_service import UsuarioService

app = QApplication(sys.argv)
app.setStyleSheet(ESTILO_GLOBAL)

janela = MainWindow()

settings = QSettings("SistemaRH", "SistemaRH")
usuario_id = settings.value("usuario_id")
if usuario_id:
    usuario_service = UsuarioService()
    usuario = usuario_service.buscar_por_id(usuario_id)
    if usuario:
        janela.mostrar_dashboard(usuario.nome)

janela.show()
sys.exit(app.exec())