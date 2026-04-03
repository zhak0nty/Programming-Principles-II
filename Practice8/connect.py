from pathlib import Path

import psycopg2

from config import DB_CONFIG


def _split_sql_statements(sql: str):
    parts = []
    buf = []
    i = 0
    n = len(sql)
    while i < n:
        if i + 1 < n and sql[i : i + 2] == "$$":
            j = i + 2
            while j + 1 < n:
                if sql[j : j + 2] == "$$":
                    buf.append(sql[i : j + 2])
                    i = j + 2
                    break
                j += 1
            else:
                buf.append(sql[i:])
                i = n
            continue
        if sql[i] == ";":
            stmt = "".join(buf).strip()
            if stmt:
                parts.append(stmt + ";")
            buf = []
            i += 1
            continue
        buf.append(sql[i])
        i += 1
    tail = "".join(buf).strip()
    if tail:
        parts.append(tail)
    return parts


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def ensure_schema(conn) -> None:
    base = Path(__file__).resolve().parent
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
    for name in ("functions.sql", "procedures.sql"):
        path = base / name
        text = path.read_text(encoding="utf-8")
        for stmt in _split_sql_statements(text):
            with conn.cursor() as cur:
                cur.execute(stmt)
        conn.commit()
