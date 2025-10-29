from app.repositories.usuario_repository import UsuarioRepository
from app.models.usuario import Usuario

class UsuarioService:
    def __init__(self):
        self.repo = UsuarioRepository()

    def listar(self):
        return self.repo.obtener_todos()

    def obtener(self, usuario_id: int):
        return self.repo.obtener_por_id(usuario_id)

    def crear(self, nombre: str, email: str):
        if not nombre or not email:
            raise ValueError("Todos los campos son obligatorios.")
        u = Usuario(nombre=nombre.strip(), email=email.strip())
        return self.repo.crear(u)

    def actualizar(self, usuario_id: int, nombre: str, email: str):
        if not nombre or not email:
            raise ValueError("Todos los campos son obligatorios.")
        u = self.repo.obtener_por_id(usuario_id)
        if not u:
            return False
        u.nombre, u.email = nombre.strip(), email.strip()
        return self.repo.actualizar(u)

    def eliminar(self, usuario_id: int):
        return self.repo.eliminar(usuario_id)
