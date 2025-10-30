import os
from dotenv import load_dotenv

# Load variables from a .env file at project root (if present)
load_dotenv()


class Config:
    """Configuration read from environment variables with sensible defaults.

    Create a `.env` file in the project root to override defaults when running
    locally (see `.env.example`).
    """
    SECRET_KEY = os.getenv("SECRET_KEY", "smarthome-secret-key")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DB = os.getenv("MYSQL_DB", "smarthome_webcontrol")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
    # Mail settings (for password recovery)
    MAIL_SERVER = os.getenv("MAIL_SERVER", "")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "0") or 0)
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() in ("1", "true", "yes")
