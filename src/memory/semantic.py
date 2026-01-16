import sqlite3
from pathlib import Path

DB_PATH = Path("data/memory.db")

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_semantic_db():
    conn = get_conn()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS semantic_memory (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)
    conn.commit()
    conn.close()

init_semantic_db()


def write_semantic(key: str, value: str):
    conn = get_conn()
    conn.execute(
        "INSERT OR REPLACE INTO semantic_memory (key, value) VALUES (?, ?)",
        (key, value),
    )
    conn.commit()
    conn.close()


def read_semantic(key: str):
    conn = get_conn()
    cursor = conn.execute(
        "SELECT value FROM semantic_memory WHERE key = ?",
        (key,),
    )
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None
