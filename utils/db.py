import sqlite3
from threading import Lock
from config import DB_PATH

_conn = None
_lock = Lock()

def get_connection():
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        _conn.row_factory = sqlite3.Row
    return _conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS user_profile (
        user_id INTEGER PRIMARY KEY,
        consent TEXT,
        gender TEXT,
        age INTEGER,
        language TEXT,
        treatment TEXT,
        depressive TEXT,
        first_name TEXT,
        family_name TEXT,
        username TEXT,
        latitude REAL,
        longitude REAL
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS phq_answers (
        user_id INTEGER PRIMARY KEY,
        phq_0 INTEGER,
        phq_1 INTEGER,
        phq_2 INTEGER,
        phq_3 INTEGER,
        phq_4 INTEGER,
        phq_5 INTEGER,
        phq_6 INTEGER,
        phq_7 INTEGER,
        sum INTEGER,
        depression INTEGER
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS wbmms_voice (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        question_id INTEGER,
        file_unique_id TEXT,
        file_path TEXT,
        duration INTEGER,
        timestamp INTEGER,
        file_size INTEGER
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        timestamp TEXT,
        action TEXT,
        details TEXT
    )""")
    conn.commit()


def upsert_user_profile(user_info: dict):
    conn = get_connection()
    c = conn.cursor()
    columns = [
        'user_id','consent','gender','age','language','treatment','depressive',
        'first_name','family_name','username','latitude','longitude'
    ]
    values = [user_info.get(col) for col in columns]
    placeholders = ','.join(['?'] * len(columns))
    update_assignments = ','.join([f"{col}=excluded.{col}" for col in columns[1:]])
    sql = f"INSERT INTO user_profile ({','.join(columns)}) VALUES ({placeholders}) " \
          f"ON CONFLICT(user_id) DO UPDATE SET {update_assignments}"
    c.execute(sql, values)
    conn.commit()


def upsert_phq_answers(user_id: int, answers: dict):
    conn = get_connection()
    c = conn.cursor()
    cols = [f'phq_{i}' for i in range(8)]
    phq_vals = [answers.get(col) for col in cols]
    total = sum(v for v in phq_vals if isinstance(v, int))
    depression = 1 if total >= 10 else 0
    columns = ['user_id'] + cols + ['sum','depression']
    values = [user_id] + phq_vals + [total, depression]
    placeholders = ','.join(['?'] * len(columns))
    update_assignments = ','.join([f"{col}=excluded.{col}" for col in columns[1:]])
    sql = f"INSERT INTO phq_answers ({','.join(columns)}) VALUES ({placeholders}) " \
          f"ON CONFLICT(user_id) DO UPDATE SET {update_assignments}"
    c.execute(sql, values)
    conn.commit()


def insert_voice_metadata(
    user_id: int,
    question_id: int,
    file_unique_id: str,
    file_path: str,
    duration: int,
    timestamp: int,
    file_size: int,
):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO wbmms_voice (user_id, question_id, file_unique_id, file_path, duration, timestamp, file_size) "
        "VALUES (?,?,?,?,?,?,?)",
        (
            user_id,
            question_id,
            file_unique_id,
            file_path,
            duration,
            timestamp,
            file_size,
        ),
    )
    conn.commit()


def insert_log(user_id: int, timestamp: str, action: str, details: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO logs (user_id, timestamp, action, details) VALUES (?,?,?,?)",
        (user_id, timestamp, action, details)
    )
    conn.commit()


def get_voice_metadata(user_id: int | None = None):
    """Return voice metadata rows."""
    conn = get_connection()
    c = conn.cursor()
    if user_id is None:
        rows = c.execute("SELECT * FROM wbmms_voice").fetchall()
    else:
        rows = c.execute(
            "SELECT * FROM wbmms_voice WHERE user_id=?",
            (user_id,),
        ).fetchall()
    return [dict(row) for row in rows]


def delete_user_records(user_id: int) -> None:
    """Remove all database records related to a user."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM user_profile WHERE user_id=?", (user_id,))
    c.execute("DELETE FROM phq_answers WHERE user_id=?", (user_id,))
    c.execute("DELETE FROM wbmms_voice WHERE user_id=?", (user_id,))
    c.execute("DELETE FROM logs WHERE user_id=?", (user_id,))
    conn.commit()
