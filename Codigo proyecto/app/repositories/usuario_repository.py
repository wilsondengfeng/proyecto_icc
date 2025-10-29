import pymysql
from flask import current_app
from app.models.usuario import Usuario


class UsuarioRepository:
    def _get_connection(self):
        return pymysql.connect(
            host=current_app.config["MYSQL_HOST"],
            user=current_app.config["MYSQL_USER"],
            password=current_app.config["MYSQL_PASSWORD"],
            database=current_app.config["MYSQL_DB"],
            port=current_app.config["MYSQL_PORT"],
            cursorclass=pymysql.cursors.DictCursor,
        )

    def obtener_todos(self):
        con = self._get_connection()
        try:
            with con.cursor() as cur:
                cur.execute("SELECT id, nombre, email FROM usuarios ORDER BY id DESC")
                rows = cur.fetchall()
                return [Usuario.from_dict(r) for r in rows]
        finally:
            con.close()

    def obtener_por_id(self, usuario_id: int):
        con = self._get_connection()
        try:
            with con.cursor() as cur:
                cur.execute("SELECT id, nombre, email FROM usuarios WHERE id = %s", (usuario_id,))
                row = cur.fetchone()
                return Usuario.from_dict(row) if row else None
        finally:
            con.close()

    def crear(self, usuario: Usuario):
        con = self._get_connection()
        try:
            with con.cursor() as cur:
                # default password for created users in this prototype is '123456'
                cur.execute(
                    "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                    (usuario.nombre, usuario.email, '123456'),
                )
                con.commit()
                return cur.lastrowid
        finally:
            con.close()

    def actualizar(self, usuario: Usuario):
        con = self._get_connection()
        try:
            with con.cursor() as cur:
                cur.execute(
                    "UPDATE usuarios SET nombre = %s, email = %s WHERE id = %s",
                    (usuario.nombre, usuario.email, usuario.id),
                )
                con.commit()
                return cur.rowcount > 0
        finally:
            con.close()

    def eliminar(self, usuario_id: int):
        con = self._get_connection()
        try:
            with con.cursor() as cur:
                cur.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
                con.commit()
                return cur.rowcount > 0
        finally:
            con.close()
