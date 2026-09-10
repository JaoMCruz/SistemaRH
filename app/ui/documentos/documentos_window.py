from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLabel, QLineEdit, QDateEdit,
    QListWidget, QFileDialog
)

class DocumentosWindow(QWidget):
    def __init__(self, funcionario_id):
        super().__init__()
        self.funcionario_id = funcionario_id
        self.documento_service = DocumentoService()

        self.setWindowTitle("Documentos do Funcionário")
        self.setGeometry(150, 150, 500, 400)

        layout = QVBoxLayout()

        titulo = QLabel("Documentos")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #1E2761;")
        layout.addWidget(titulo)

        botao_upload = QPushButton("Enviar Documento")
        botao_upload.clicked.connect(self.enviar_documento)
        layout.addWidget(botao_upload)

        self.lista_documentos = QListWidget()
        layout.addWidget(self.lista_documentos)

        self.setLayout(layout)
        self.carregar_documentos()

    def carregar_documentos(self):
        self.lista_documentos.clear()
        documentos = self.documento_service.listar_por_funcionario(self.funcionario_id)

        for documento in documentos:
            self.lista_documentos.addItem(documento.nome_arquivo)

    def enviar_documento(self):
        caminho, _ = QFileDialog.getOpenFileName(self, "Selecionar documento")

        if not caminho:
            return

        self.documento_service.cadastrar(self.funcionario_id, caminho)
        self.carregar_documentos()