import os

DB_CONFIG = {
    "host": os.environ.get("PGHOST", "localhost"),
    "database": os.environ.get("PGDATABASE", "phonebook_db"),
    "user": os.environ.get("PGUSER", "postgres"),
    "password": os.environ.get("PGPASSWORD", "postgres"),
    "port": int(os.environ.get("PGPORT", "5432")),
}
