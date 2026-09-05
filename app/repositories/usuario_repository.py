from app.database.conexao import get_session
from app.models.usuario import Usuario

Class UsuarioRepository:
    def __init__(self):
        self.session = get_session()
        usuario = session.query(Usuario).filter_by(Usuario.email == email).first()
        session.close()
