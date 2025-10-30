# 1. Requisitos Previos

Python 3.8 o superior instalado
MySQL Server instalado y ejecutándose
pip (gestor de paquetes de Python)

# 2 Crear el proyecto

# Crear directorio del proyecto
mkdir FLASK
cd FLASK

# Crear la estructura de carpetas
mkdir -p app/{models,repositories,services,controllers,templates,static/css}

# 3 crear la base de datos

## Configuración de la base de datos local (.env + XAMPP)

Para que la aplicación lea tu base de datos local (MariaDB en XAMPP) y otras variables
de entorno, crea o edita el archivo `.env` en la raíz del proyecto. Ya incluimos un
archivo de ejemplo `.env.example` y un `.env` por defecto que puedes adaptar.

Valores típicos para XAMPP (por defecto en `.env`):

SECRET_KEY=change-me-to-a-secret
MYSQL_HOST=127.0.0.1
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DB=smarthome_webcontrol
MYSQL_PORT=3306

Pasos rápidos (PowerShell):

```powershell
.\env\Scripts\Activate.ps1
pip install -r requirements.txt
# Si prefieres usar el ejemplo:
copy .env.example .env
# Edita .env y luego ejecuta la app
python run.py
```

Con esto, las llamadas a `current_app.config["MYSQL_HOST"]`, etc., leerán los valores
definidos y los repositorios podrán conectarse a tu base de datos local.

