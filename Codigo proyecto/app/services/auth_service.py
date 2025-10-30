from app.repositories.auth_user_repository import AuthUserRepository
from app.models.auth_user import AuthUser
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, url_for, request
import logging
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
import smtplib
from email.message import EmailMessage

class AuthService:
    def __init__(self):
        self.repo = AuthUserRepository()

    def validar_login(self, email: str, password: str):
        """Retorna el usuario si (email,password) válidos, si no None."""
        user = self.repo.obtener_por_email(email.strip())
        if not user:
            # Use Flask app logger so messages appear in the console during `flask run` / app.run(debug=True)
            try:
                current_app.logger.debug(f"validar_login: usuario no encontrado para email={email}")
            except Exception:
                pass
            return None

        stored = (user.password or "").strip()

        # Intento seguro de verificación
        try:
            try:
                current_app.logger.debug(f"validar_login: stored repr={repr(stored)[:200]} for email={email}")
                current_app.logger.debug(f"validar_login: stored contains $: {'$' in stored}")
                parts = stored.split('$')
                current_app.logger.debug(f"validar_login: split parts count={len(parts)} (first part preview: {parts[0] if parts else None})")
            except Exception:
                pass

            result = check_password_hash(stored, password)
            try:
                current_app.logger.debug(f"validar_login: check_password_hash result={result} for email={email}")
            except Exception:
                pass
            if result:
                try:
                    current_app.logger.debug(f"validar_login: password verificado por hash para email={email}")
                except Exception:
                    pass
                return user
        except Exception as exc:
            # En caso de que stored no tenga el formato esperado para check_password_hash
            try:
                current_app.logger.debug(f"validar_login: check_password_hash raised for email={email}: {exc}")
            except Exception:
                pass

        # Normalizar posibles comillas alrededor del valor almacenado y comparar en texto plano
        normalized = stored.strip("'\"")
        if normalized == password:
            # Migración: hashear y actualizar la DB
            hashed = generate_password_hash(password)
            try:
                updated = self.repo.actualizar_password(user.id, hashed, user.is_admin)
                if updated:
                    user.password = hashed
                    try:
                        current_app.logger.debug(f"validar_login: contraseña migrada a hash para user_id={user.id}")
                    except Exception:
                        pass
            except Exception as exc:
                try:
                    current_app.logger.warning(f"validar_login: fallo al actualizar password para user_id={user.id}: {exc}")
                except Exception:
                    pass
            return user

        try:
            current_app.logger.debug(f"validar_login: credenciales inválidas para email={email}")
        except Exception:
            pass
        return None

    def crear_usuario(self, nombre: str, email: str, password: str, is_admin: bool = False):
        """Crea un nuevo usuario en el sistema."""
        # Hashear la contraseña antes de persistir
        hashed = generate_password_hash(password)
        user = self.repo.obtener_por_email(email)
        if user:
            return None  # El email ya está en uso
        
        nuevo_usuario = {
            "nombre": nombre,
            "email": email,
            "password": hashed,
            "is_admin": is_admin
        }
        return self.repo.crear_usuario(AuthUser.from_dict(nuevo_usuario))

    def listar_usuarios(self):
        """Retorna la lista de usuarios (no administradores)"""
        return self.repo.listar_usuarios()

    # --- Password reset / email helpers ---
    def _get_serializer(self):
        secret = current_app.config.get("SECRET_KEY")
        return URLSafeTimedSerializer(secret)

    def generate_reset_token(self, email: str) -> str:
        s = self._get_serializer()
        return s.dumps(email, salt="password-reset-salt")

    def verify_reset_token(self, token: str, max_age: int = 3600) -> str | None:
        s = self._get_serializer()
        try:
            email = s.loads(token, salt="password-reset-salt", max_age=max_age)
            return email
        except SignatureExpired:
            return None
        except BadSignature:
            return None

    def send_reset_email(self, email: str) -> bool:
        """Genera token y envía email con enlace de recuperación. Retorna True si enviado o queued."""
        token = self.generate_reset_token(email)
        # Intentar construir URL completa usando url_for si hay contexto de request
        reset_url = None
        try:
            # Si estamos en una request activa, url_for con _external construirá el host correctamente
            reset_url = url_for('auth.reset_password', token=token, _external=True)
        except Exception:
            # No hay contexto de request o url_for falló; construir manualmente con fallback seguro
            server_name = current_app.config.get('SERVER_NAME') or '127.0.0.1:5000'
            # Asegurarnos de no crear 'http://None'
            reset_url = f"http://{server_name}/reset_password/{token}"
        subject = "Recuperación de contraseña - SmartHome"
        body = f"Hola,\n\nPara restablecer tu contraseña haz clic en el siguiente enlace:\n{reset_url}\n\nSi no solicitaste esto, ignora este correo.\n"

        mail_server = current_app.config.get("MAIL_SERVER")
        mail_port = current_app.config.get("MAIL_PORT")
        username = current_app.config.get("MAIL_USERNAME")
        password = current_app.config.get("MAIL_PASSWORD")
        use_tls = current_app.config.get("MAIL_USE_TLS", True)

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = username or "no-reply@smarthome.local"
        msg["To"] = email
        msg.set_content(body)

        # If SMTP not configured, fallback to printing the message in the app log
        if not mail_server or not mail_port:
            try:
                current_app.logger.info("send_reset_email: SMTP not configured; printing reset URL to console")
            except Exception:
                pass
            print("--- Password reset (development) ---")
            print(body)
            print("------------------------------------")
            return True

        try:
            if use_tls:
                server = smtplib.SMTP(mail_server, mail_port, timeout=10)
                server.starttls()
            else:
                server = smtplib.SMTP(mail_server, mail_port, timeout=10)

            if username and password:
                server.login(username, password)
            server.send_message(msg)
            server.quit()
            return True
        except Exception as exc:
            try:
                current_app.logger.warning(f"send_reset_email: fallo al enviar email: {exc}")
            except Exception:
                pass
            return False

    def reset_password_with_token(self, token: str, new_password: str) -> bool:
        email = self.verify_reset_token(token)
        if not email:
            return False
        user = self.repo.obtener_por_email(email)
        if not user:
            return False
        hashed = generate_password_hash(new_password)
        return self.repo.actualizar_password(user.id, hashed, user.is_admin)
