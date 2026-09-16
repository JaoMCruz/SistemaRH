import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSettings

from app.ui.boas_vindas.boas_vindas_window import BoasVindasWindow
from app.ui.dashboard.dashboard_window import DashboardWindow
from app.services.usuario_service import UsuarioService

app = QApplication(sys.argv)

settings = QSettings("SistemaRH", "SistemaRH")
usuario_id = settings.value("usuario_id")

if usuario_id:
    usuario_service = UsuarioService()
    usuario = usuario_service.buscar_por_id(usuario_id)

    if usuario:
        janela = DashboardWindow(usuario.nome)
    else:
        janela = BoasVindasWindow()
else:
    janela = BoasVindasWindow()

janela.show()
sys.exit(app.exec())