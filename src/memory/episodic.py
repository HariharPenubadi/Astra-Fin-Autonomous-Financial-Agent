import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("data/episodic.db")

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_episodic_db():
    conn = get_conn()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS episodes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        user_query TEXT,
        assistant_response TEXT
    )
    """)
    conn.commit()
    conn.close()

init_episodic_db()

def store_episode(user_query: str, assistant_response: str):
    conn = get_conn()
    conn.execute(
        "INSERT INTO episodes (timestamp, user_query, assistant_response) VALUES (?, ?, ?)",
        (datetime.utcnow().isoformat(), user_query, assistant_response),
    )
    conn.commit()
    conn.close()

def recall_episodes(limit: int = 5):
    conn = get_conn()
    cursor = conn.execute(
        "SELECT user_query, assistant_response FROM episodes ORDER BY id DESC LIMIT ?",
        (limit,),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows
