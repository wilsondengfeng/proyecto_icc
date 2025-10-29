from app.repositories.dispositivo_repository import DispositivoRepository
from app.models.dispositivo import Dispositivo


class DispositivoService:
    def __init__(self):
        self.repo = DispositivoRepository()

    def listar_todos(self):
        return self.repo.obtener_todos()

    def obtener(self, dispositivo_id: int):
        return self.repo.obtener_por_id(dispositivo_id)

    def listar_por_usuario(self, usuario_id: int):
        return self.repo.obtener_por_usuario(usuario_id)

    def crear(self, nombre: str, tipo: str, usuario_id: int = None):
        d = Dispositivo(nombre=nombre, tipo=tipo, estado=False, usuario_id=usuario_id)
        return self.repo.crear(d)

    def actualizar(self, dispositivo: Dispositivo):
        return self.repo.actualizar(dispositivo)

    def eliminar(self, dispositivo_id: int):
        return self.repo.eliminar(dispositivo_id)

    def toggle_estado(self, dispositivo_id: int):
        return self.repo.toggle_estado(dispositivo_id)
