import pymysql
from flask import current_app
from app.models.auth_user import AuthUser

class AuthUserRepository:
    def _get_connection(self):
        return pymysql.connect(
            host=current_app.config["MYSQL_HOST"],
            user=current_app.config["MYSQL_USER"],
            password=current_app.config["MYSQL_PASSWORD"],
            database=current_app.config["MYSQL_DB"],
            port=current_app.config["MYSQL_PORT"],
            cursorclass=pymysql.cursors.DictCursor
        )

    def obtener_por_email(self, email: str):
        con = self._get_connection()
        try:
            with con.cursor() as cur:
                # Primero buscar en la tabla admin
                cur.execute("SELECT id, nombre, email, password, TRUE as is_admin FROM admin WHERE email = %s", (email,))
                row = cur.fetchone()
                if row:
                    return AuthUser.from_dict(row)
                
                # Si no está en admin, buscar en usuarios
                cur.execute("SELECT id, nombre, email, password, FALSE as is_admin FROM usuarios WHERE email = %s", (email,))
                row = cur.fetchone()
                return AuthUser.from_dict(row) if row else None
        finally:
            con.close()

    def obtener_por_id(self, user_id: int, is_admin: bool = False):
        con = self._get_connection()
        try:
            with con.cursor() as cur:
                if is_admin:
                    table = "admin"
                else:
                    table = "usuarios"
                cur.execute(f"SELECT id, nombre, email, password FROM {table} WHERE id = %s", (user_id,))
                row = cur.fetchone()
                if row:
                    row["is_admin"] = is_admin
                return AuthUser.from_dict(row) if row else None
        finally:
            con.close()

    def crear_usuario(self, auth_user: AuthUser):
        con = self._get_connection()
        try:
            with con.cursor() as cur:
                if auth_user.is_admin:
                    table = "admin"
                else:
                    table = "usuarios"
                cur.execute(
                    f"INSERT INTO {table} (nombre, email, password) VALUES (%s, %s, %s)",
                    (auth_user.nombre, auth_user.email, auth_user.password)
                )
                con.commit()
                return cur.lastrowid
        finally:
            con.close()

    def listar_usuarios(self):
        con = self._get_connection()
        try:
            with con.cursor() as cur:
                cur.execute("SELECT id, nombre, email, FALSE as is_admin FROM usuarios")
                rows = cur.fetchall()
                return [AuthUser.from_dict(row) for row in rows]
        finally:
            con.close()
