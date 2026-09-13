from app.database.conexao import get_session
from app.models.documento import Documento

class DocumentoRepository:
    def listar_por_funcionario(self, funcionario_id):
        session = get_session()
        documentos = session.query(Documento).filter(Documento.funcionario_id == funcionario_id).all()
        session.close()
        return documentos

    def cadastrar(self, documento):
        session = get_session()
        session.add(documento)
        session.commit()
        session.close()

    def listar_todos(self):
        session = get_session()
        documentos = session.query(Documento).all()
        session.close()
        return documentos

    def excluir(self, documento_id):
        session = get_session()
        documento = session.query(Documento).filter(Documento.id == documento_id).first()
        session.delete(documento)
        session.commit()
        session.close()

    def buscar_por_id(self, documento_id):
        session = get_session()
        documento = session.query(Documento).filter(Documento.id == documento_id).first()
        session.close()
        return documento

    def contar_por_funcionario(self, funcionario_id):
        session = get_session()
        total = session.query(Documento).filter(Documento.funcionario_id == funcionario_id).count()
        session.close()
        return total