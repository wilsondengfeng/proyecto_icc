import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "smarthome-secret-key")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DB = os.getenv("MYSQL_DB", "smarthome_webcontrol")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
