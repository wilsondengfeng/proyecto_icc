class AuthUser:
    def __init__(self, id=None, nombre=None, email=None, password=None, is_admin=False):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "password": self.password,
            "is_admin": self.is_admin
        }

    @staticmethod
    def from_dict(data: dict):
        if not data:
            return None
        return AuthUser(
            id=data.get("id"),
            nombre=data.get("nombre"),
            email=data.get("email"),
            password=data.get("password"),
            is_admin=data.get("is_admin", False)
        )
