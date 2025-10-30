# SmartHome - Panel de control de dispositivos IoT

## Tecnologías Utilizadas

- Python 3.8+
- Flask
- PyMySQL (MySQL/MariaDB)
- Jinja2 (templates)
- Werkzeug (hashing de contraseñas)
- python-dotenv (variables de entorno)

## Instalación (Paso a paso para correr la app localmente)

1. Clona el repositorio y abre una terminal en la raíz del proyecto.

2. Crear el entorno virtual:

```powershell
py -m venv env
```

3. Activar el entorno virtual:

```powershell
env\Scripts\activate
```

4. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

5. Configurar variables de entorno y ejecutar la aplicación:

```powershell
copy .env.example .env
# Edita .env con tus valores (SECRET_KEY, MYSQL_*, MAIL_* si corresponde)
python run.py
```

La aplicación queda disponible por defecto en http://127.0.0.1:5000

## Configuración del Entorno (opcional)

- Crea y edita un archivo `.env` en la raíz. Hay un `.env.example` con las claves típicas.
- Variables relevantes:
  - `SECRET_KEY` — clave para firmar sesiones y tokens.
  - `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DB`, `MYSQL_PORT` — conexión a la BD.
  - `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_USE_TLS` — (opcional) SMTP para enviar correos.
  - `SERVER_NAME` — (opcional) host:port que se usará para construir URLs en correos cuando no haya contexto HTTP.

Nota: si `SERVER_NAME` existe pero es `None`, la aplicación intentará usar la dirección de la petición; si no hay petición usará `127.0.0.1:5000` como fallback.

## Cómo probar la funcionalidad

- Inicia la app y abre `/login` para probar autenticación.
- El panel `/dashboard` muestra vistas diferentes según si eres admin o usuario.
- Recuperar contraseña:
  - En la pantalla de login haz clic en "¿Olvidaste tu contraseña?" y envía el correo.
  - Si SMTP está configurado, recibirás un correo con el enlace de restablecimiento.
  - Si NO hay SMTP configurado, la aplicación imprimirá el enlace de recuperación en la terminal donde ejecutaste `python run.py`. Busca un bloque como:

    --- Password reset (development) ---
    http://127.0.0.1:5000/reset_password/<token>
    ------------------------------------

  - Abre el enlace en el navegador para cambiar la contraseña.

- Si importas datos iniciales con contraseñas, usa `app/database_hashed.sql` para evitar truncamiento de hashes.

## Estructura del proyecto (rápido)

- `run.py` — entrada de la app.
- `app/config.py` — carga de `.env` y configuración.
- `app/controllers/` — rutas y controladores.
- `app/services/` — lógica de negocio (auth, usuarios, dispositivos).
- `app/repositories/` — acceso a la base de datos.
- `app/templates/` — plantillas HTML.

## Capturas de Pantalla o Gif de la aplicación

Próximamente: añade aquí tus capturas o GIFs.

## Notas adicionales

- Hay un script (`scripts/generate_hashed_sql.py`) para generar un `database_hashed.sql` con contraseñas hasheadas si necesitas reimportar datos.
- Si quieres integración de correo más robusta, puedo añadir Flask-Mail y plantillas HTML para los correos.
- Si quieres, añado una sección de credenciales de ejemplo (solo para desarrollo) o guías para importar la BD en XAMPP/MariaDB.
