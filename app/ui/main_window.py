from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget

from app.ui.boas_vindas.boas_vindas_window import BoasVindasWindow
from app.ui.login.login_window import LoginWindow
from app.ui.dashboard.dashboard_window import DashboardWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de RH")
        self.setGeometry(100, 100, 1150, 650)

        self.pagina_dashboard = None

        self.stack = QStackedWidget()

        self.pagina_boas_vindas = BoasVindasWindow(callback_entrar=self.mostrar_login)
        self.pagina_login = LoginWindow(callback_login_sucesso=self.mostrar_dashboard)

        self.stack.addWidget(self.pagina_boas_vindas)  # 0
        self.stack.addWidget(self.pagina_login)          # 1

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stack)
        self.setLayout(layout)

    def mostrar_boas_vindas(self):
        self.stack.setCurrentWidget(self.pagina_boas_vindas)

    def mostrar_login(self):
        self.pagina_login.limpar_campos()
        self.stack.setCurrentWidget(self.pagina_login)

    def mostrar_dashboard(self, nome_usuario):
        if self.pagina_dashboard is not None:
            self.stack.removeWidget(self.pagina_dashboard)
            self.pagina_dashboard.deleteLater()

        self.pagina_dashboard = DashboardWindow(nome_usuario, callback_sair=self.mostrar_boas_vindas)
        self.stack.addWidget(self.pagina_dashboard)
        self.stack.setCurrentWidget(self.pagina_dashboard)