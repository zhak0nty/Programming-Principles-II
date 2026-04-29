import os


def _default_db_user():
    return (
        os.environ.get("PGUSER")
        or os.environ.get("USER")
        or os.environ.get("USERNAME")
        or "postgres"
    )


DB_CONFIG = {
    "host": os.environ.get("PGHOST", "localhost"),
    "database": os.environ.get("PGDATABASE", "phonebook_db"),
    "user": _default_db_user(),
    "password": os.environ.get("PGPASSWORD", ""),
    "port": int(os.environ.get("PGPORT", "5432")),
}
