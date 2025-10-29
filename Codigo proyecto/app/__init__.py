from flask import Flask
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Rutas
    from app.controllers.auth_controller import bp as auth_bp
    from app.controllers.usuarios_controller import bp as usuarios_bp
    from app.controllers.dispositivos_controller import bp as dispositivos_bp

    app.register_blueprint(auth_bp)                      # /login
    app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
    app.register_blueprint(dispositivos_bp, url_prefix="/dispositivos")
    return app
