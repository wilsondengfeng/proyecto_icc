from flask import Flask
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # Asegurar logging en nivel DEBUG para que current_app.logger.debug(...) se muestre
    import logging
    app.logger.setLevel(logging.DEBUG)

    # Instanciar servicios y adjuntarlos a la app (evita instanciación en import-time)
    from app.services.auth_service import AuthService
    from app.services.dispositivo_service import DispositivoService
    from app.services.usuario_service import UsuarioService

    app.auth_service = AuthService()
    app.dispositivo_service = DispositivoService()
    app.usuario_service = UsuarioService()

    # Rutas (importar después de configurar la app)
    from app.controllers.auth_controller import bp as auth_bp
    from app.controllers.usuarios_controller import bp as usuarios_bp
    from app.controllers.dispositivos_controller import bp as dispositivos_bp

    app.register_blueprint(auth_bp)                      # /login
    app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
    app.register_blueprint(dispositivos_bp, url_prefix="/dispositivos")
    return app
