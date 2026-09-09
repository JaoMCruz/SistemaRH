import bcrypt
from app.repositories.usuario_repository import UsuarioRepository

class UsuarioService:
    def __init__(self):
        self.repository = UsuarioRepository()


    def autenticar (self, email, senha):
        usuario = self.repository.buscar_por_email(email)

        if usuario is None:
            return None

        senha_correta = bcrypt.checkpw(senha.encode('utf-8'), usuario.senha.encode('utf-8'))

        if not senha_correta:
            return None

        return usuario