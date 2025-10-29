class Dispositivo:
    def __init__(self, id=None, nombre=None, tipo=None, estado=False, usuario_id=None):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo
        self.estado = bool(estado)
        self.usuario_id = usuario_id

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "estado": self.estado,
            "usuario_id": self.usuario_id,
        }

    @staticmethod
    def from_dict(data: dict):
        if not data:
            return None
        return Dispositivo(
            id=data.get("id"),
            nombre=data.get("nombre"),
            tipo=data.get("tipo"),
            estado=data.get("estado"),
            usuario_id=data.get("usuario_id"),
        )
