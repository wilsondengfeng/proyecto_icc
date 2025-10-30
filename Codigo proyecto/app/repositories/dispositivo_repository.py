import pymysql
from flask import current_app
from app.models.dispositivo import Dispositivo

class DispositivoRepository:
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
                cur.execute("SELECT id, nombre, tipo, estado, usuario_id FROM dispositivos ORDER BY id DESC")
                rows = cur.fetchall()
                return [Dispositivo.from_dict(r) for r in rows]
        finally:
            con.close()

    def obtener_por_id(self, dispositivo_id: int):
        con = self._get_connection()
        try:
            with con.cursor() as cur:
                cur.execute("SELECT id, nombre, tipo, estado, usuario_id FROM dispositivos WHERE id = %s", (dispositivo_id,))
                row = cur.fetchone()
                return Dispositivo.from_dict(row) if row else None
        finally:
            con.close()

    def obtener_por_usuario(self, usuario_id: int):
        con = self._get_connection()
        try:
            with con.cursor() as cur:
                cur.execute("SELECT id, nombre, tipo, estado, usuario_id FROM dispositivos WHERE usuario_id = %s ORDER BY id DESC", (usuario_id,))
                rows = cur.fetchall()
                return [Dispositivo.from_dict(r) for r in rows]
        finally:
            con.close()

    def crear(self, dispositivo: Dispositivo):
        con = self._get_connection()
        try:
            with con.cursor() as cur:
                cur.execute(
                    "INSERT INTO dispositivos (nombre, tipo, estado, usuario_id) VALUES (%s, %s, %s, %s)",
                    (dispositivo.nombre, dispositivo.tipo, int(dispositivo.estado), dispositivo.usuario_id),
                )
                con.commit()
                return cur.lastrowid
        finally:
            con.close()

    def actualizar(self, dispositivo: Dispositivo):
        con = self._get_connection()
        try:
            with con.cursor() as cur:
                cur.execute(
                    "UPDATE dispositivos SET nombre=%s, tipo=%s, estado=%s, usuario_id=%s WHERE id=%s",
                    (dispositivo.nombre, dispositivo.tipo, int(dispositivo.estado), dispositivo.usuario_id, dispositivo.id),
                )
                con.commit()
                return cur.rowcount > 0
        finally:
            con.close()

    def eliminar(self, dispositivo_id: int):
        con = self._get_connection()
        try:
            with con.cursor() as cur:
                cur.execute("DELETE FROM dispositivos WHERE id = %s", (dispositivo_id,))
                con.commit()
                return cur.rowcount > 0
        finally:
            con.close()

    def toggle_estado(self, dispositivo_id: int):
        con = self._get_connection()
        try:
            with con.cursor() as cur:
                cur.execute("SELECT estado FROM dispositivos WHERE id = %s", (dispositivo_id,))
                row = cur.fetchone()
                if not row:
                    return None
                nuevo = 0 if row.get("estado") else 1
                cur.execute("UPDATE dispositivos SET estado = %s WHERE id = %s", (nuevo, dispositivo_id))
                con.commit()
                return bool(nuevo)
        finally:
            con.close()
