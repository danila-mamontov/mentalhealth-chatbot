import sqlite3
from contextlib import contextmanager
from config import DB_PATH


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users (
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
        )"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS phq_answers (
            user_id INTEGER,
            question_id INTEGER,
            answer INTEGER,
            PRIMARY KEY(user_id, question_id),
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS voice_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            question_id INTEGER,
            file_unique_id TEXT,
            file_path TEXT,
            timestamp INTEGER,
            duration INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            timestamp TEXT,
            action TEXT,
            details TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )"""
    )
    conn.commit()
    conn.close()


@contextmanager
def get_cursor():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        yield cursor
        conn.commit()
    finally:
        conn.close()


def upsert_user(info: dict):
    columns = [
        "user_id",
        "consent",
        "gender",
        "age",
        "language",
        "treatment",
        "depressive",
        "first_name",
        "family_name",
        "username",
        "latitude",
        "longitude",
    ]
    values = [info.get(col) for col in columns]
    placeholders = ",".join("?" for _ in columns)
    with get_cursor() as cur:
        cur.execute(
            f"INSERT INTO users ({','.join(columns)}) VALUES ({placeholders}) "
            "ON CONFLICT(user_id) DO UPDATE SET "
            + ",".join(f"{c}=excluded.{c}" for c in columns[1:]),
            values,
        )


def save_phq_answers(user_id: int, answers: dict):
    with get_cursor() as cur:
        for qid, ans in answers.items():
            cur.execute(
                "INSERT OR REPLACE INTO phq_answers (user_id, question_id, answer) "
                "VALUES (?, ?, ?)",
                (user_id, qid, ans),
            )


def save_voice_metadata(entries: list):
    """entries is list of dict with keys user_id, question_id, file_unique_id, file_path, timestamp, duration"""
    with get_cursor() as cur:
        for e in entries:
            cur.execute(
                """INSERT INTO voice_metadata (user_id, question_id, file_unique_id, file_path, timestamp, duration)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    e["user_id"],
                    e["question_id"],
                    e["file_unique_id"],
                    e["file_path"],
                    e["timestamp"],
                    e["duration"],
                ),
            )
