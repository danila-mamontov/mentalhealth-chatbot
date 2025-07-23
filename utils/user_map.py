import sqlite3
from threading import Lock
from config import ID_DB_PATH

_conn = None
_lock = Lock()


def get_connection():
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(ID_DB_PATH, check_same_thread=False)
        _conn.row_factory = sqlite3.Row
    return _conn


def init_user_map():
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS user_map (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE
        )"""
    )
    conn.commit()


def get_user_id(telegram_id: int) -> int:
    conn = get_connection()
    row = conn.execute(
        "SELECT user_id FROM user_map WHERE telegram_id=?",
        (telegram_id,),
    ).fetchone()
    if row:
        return row["user_id"]
    cur = conn.execute(
        "INSERT INTO user_map (telegram_id) VALUES (?)",
        (telegram_id,),
    )
    conn.commit()
    return cur.lastrowid


def get_telegram_id(user_id: int) -> int | None:
    row = get_connection().execute(
        "SELECT telegram_id FROM user_map WHERE user_id=?",
        (user_id,),
    ).fetchone()
    return row["telegram_id"] if row else None
