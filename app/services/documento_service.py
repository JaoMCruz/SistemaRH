import os
import shutil
import uuid

from app.repositories.documento_repository import DocumentoRepository
from app.models.documento import Documento

PASTA_DOCUMENTOS = "documentos_armazenados"


class DocumentoService:

    def __init__(self):
        self.repository = DocumentoRepository()
        os.makedirs(PASTA_DOCUMENTOS, exist_ok=True)

    def listar_por_funcionario(self, funcionario_id):
        return self.repository.listar_por_funcionario(funcionario_id)

    def cadastrar(self, funcionario_id, caminho_original):
        nome_arquivo = os.path.basename(caminho_original)
        nome_unico = f"{uuid.uuid4().hex}_{nome_arquivo}"
        destino = os.path.join(PASTA_DOCUMENTOS, nome_unico)

        shutil.copy2(caminho_original, destino)

        documento = Documento(
            funcionario_id=funcionario_id,
            nome_arquivo=nome_arquivo,
            caminho_arquivo=destino
        )

        self.repository.cadastrar(documento)

    def listar_todos(self):
        return self.repository.listar_todos()

    def excluir(self, documento_id):
        self.repository.excluir(documento_id)

    def buscar_por_id(self, documento_id):
        return self.repository.buscar_por_id(documento_id)