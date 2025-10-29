from app.repositories.auth_user_repository import AuthUserRepository
from app.models.auth_user import AuthUser
from werkzeug.security import generate_password_hash, check_password_hash

class AuthService:
    def __init__(self):
        self.repo = AuthUserRepository()

    def validar_login(self, email: str, password: str):
        """Retorna el usuario si (email,password) válidos, si no None."""
        user = self.repo.obtener_por_email(email.strip())
        if user and user.password == password:  # TODO: Implementar hashing de contraseñas
            return user
        return None

    def crear_usuario(self, nombre: str, email: str, password: str, is_admin: bool = False):
        """Crea un nuevo usuario en el sistema."""
        # TODO: Implementar hashing de contraseñas
        user = self.repo.obtener_por_email(email)
        if user:
            return None  # El email ya está en uso
        
        nuevo_usuario = {
            "nombre": nombre,
            "email": email,
            "password": password,
            "is_admin": is_admin
        }
        return self.repo.crear_usuario(AuthUser.from_dict(nuevo_usuario))

    def listar_usuarios(self):
        """Retorna la lista de usuarios (no administradores)"""
        return self.repo.listar_usuarios()
