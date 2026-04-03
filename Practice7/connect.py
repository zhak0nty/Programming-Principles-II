import psycopg2

from config import DB_CONFIG


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def ensure_schema(conn) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NOT NULL DEFAULT '',
                phone VARCHAR(64) NOT NULL
            );
            """
        )
    conn.commit()
