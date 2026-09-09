from app.database.conexao import get_session
from app.models.usuario import Usuario

class UsuarioRepository:
    def buscar_por_email(self, email):
        session = get_session()
        usuario = session.query(Usuario).filter(Usuario.email == email).first()
        session.close()
        return usuario