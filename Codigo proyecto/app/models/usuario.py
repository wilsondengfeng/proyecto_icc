class Usuario:
    def __init__(self, id=None, nombre=None, email=None):
        self.id = id
        self.nombre = nombre
        self.email = email

    def to_dict(self):
        return {"id": self.id, "nombre": self.nombre, "email": self.email}

    @staticmethod
    def from_dict(data: dict):
        if not data:
            return None
        return Usuario(
            id=data.get("id"),
            nombre=data.get("nombre"),
            email=data.get("email")
        )
