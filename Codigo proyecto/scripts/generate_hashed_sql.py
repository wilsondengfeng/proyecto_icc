"""
Generador de SQL con contraseñas hasheadas.

Uso:
  - Activar el entorno virtual: .\env\Scripts\Activate.ps1
  - Ejecutar: python scripts/generate_hashed_sql.py

Este script lee `app/database.sql`, busca las sentencias INSERT para `admin` y `usuarios` y genera
un archivo `app/database_hashed.sql` con las contraseñas reemplazadas por hashes generados con
werkzeug.security.generate_password_hash (compatibles con check_password_hash usado en la app).

NOTA: Revisa el archivo resultante antes de importarlo en MariaDB/XAMPP.
"""
import re
from pathlib import Path
from werkzeug.security import generate_password_hash

ROOT = Path(__file__).resolve().parents[1]
SRC_SQL = ROOT / "app" / "database.sql"
OUT_SQL = ROOT / "app" / "database_hashed.sql"

if not SRC_SQL.exists():
    print(f"Archivo fuente no encontrado: {SRC_SQL}")
    raise SystemExit(1)

content = SRC_SQL.read_text(encoding="utf-8")

# Reemplazar contraseñas en INSERT INTO admin (...) VALUES (...)
# patrón sencillo para capturar la tupla entre paréntesis en valores individuales
def hash_values_in_insert(sql_text, table_name):
    # Captura la cláusula VALUES (todo lo que vaya hasta el punto y coma)
    pattern = re.compile(rf"(INSERT INTO\s+{table_name}\s*\([^)]*\)\s*VALUES\s*)(.*?);", re.IGNORECASE | re.DOTALL)

    def repl(match):
        prefix = match.group(1)
        values_block = match.group(2).strip()

        # Encontrar todas las tuplas dentro del bloque VALUES: (...) , (...) , ...
        tuples = re.findall(r"\([^()]*\)", values_block, re.DOTALL)
        new_tuples = []
        for t in tuples:
            inner = t[1:-1].strip()
            # split por comas respetando comillas simples
            parts = [p.strip() for p in re.split(r",(?=(?:[^']*'[^']*')*[^']*$)", inner)]
            if len(parts) < 1:
                new_tuples.append(t)
                continue
            raw_pw = parts[-1]
            m = re.match(r"'(?P<pw>.*)'", raw_pw)
            pw = m.group('pw') if m else raw_pw.strip()
            hashed = generate_password_hash(pw)
            parts[-1] = f"'{hashed}'"
            new_tuple = "(" + ", ".join(parts) + ")"
            new_tuples.append(new_tuple)

        new_values_block = ", ".join(new_tuples)
        return prefix + new_values_block + ";"

    new_sql = pattern.sub(repl, sql_text)
    return new_sql

content_hashed = hash_values_in_insert(content, "admin")
content_hashed = hash_values_in_insert(content_hashed, "usuarios")

OUT_SQL.write_text(content_hashed, encoding="utf-8")
print(f"Archivo generado: {OUT_SQL}")
print("Revisa el archivo antes de importarlo en MariaDB/XAMPP.")
