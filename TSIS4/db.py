from __future__ import annotations

from typing import Any

import psycopg2

from config import DB_CONFIG


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS players (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS game_sessions (
    id SERIAL PRIMARY KEY,
    player_id INTEGER REFERENCES players(id),
    score INTEGER NOT NULL,
    level_reached INTEGER NOT NULL,
    played_at TIMESTAMP DEFAULT NOW()
);
"""


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def init_db() -> None:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(SCHEMA_SQL)
        conn.commit()
    finally:
        conn.close()


def _get_or_create_player(cur, username: str) -> int:
    cur.execute("SELECT id FROM players WHERE username = %s", (username,))
    row = cur.fetchone()
    if row:
        return int(row[0])
    cur.execute("INSERT INTO players (username) VALUES (%s) RETURNING id", (username,))
    return int(cur.fetchone()[0])


def save_game_result(username: str, score: int, level_reached: int) -> None:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            pid = _get_or_create_player(cur, username)
            cur.execute(
                "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
                (pid, score, level_reached),
            )
        conn.commit()
    finally:
        conn.close()


def fetch_top10() -> list[dict[str, Any]]:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT p.username, g.score, g.level_reached, g.played_at
                FROM game_sessions g
                JOIN players p ON p.id = g.player_id
                ORDER BY g.score DESC, g.played_at DESC
                LIMIT 10
                """
            )
            rows = cur.fetchall()
    finally:
        conn.close()
    return [
        {
            "username": r[0],
            "score": int(r[1]),
            "level_reached": int(r[2]),
            "played_at": r[3].strftime("%Y-%m-%d %H:%M"),
        }
        for r in rows
    ]


def fetch_personal_best(username: str) -> int:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT MAX(g.score)
                FROM game_sessions g
                JOIN players p ON p.id = g.player_id
                WHERE p.username = %s
                """,
                (username,),
            )
            row = cur.fetchone()
    finally:
        conn.close()
    return int(row[0] or 0)
