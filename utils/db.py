import sqlite3
from threading import Lock
from config import DB_PATH

# Supported language codes for statistics
LANGS = ["en", "de", "ru", "fr", "zh", "hi", "ar"]

# Age ranges used for aggregation (label, start, end)
AGE_RANGES = [
    ("18_29", 18, 29),
    ("30_39", 30, 39),
    ("40_49", 40, 49),
    ("50_59", 50, 59),
    ("60_69", 60, 69),
    ("70_79", 70, 79),
    ("80_89", 80, 89),
    ("90_plus", 90, None),
]

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

    c.execute("""CREATE TABLE IF NOT EXISTS stats (
        id INTEGER PRIMARY KEY CHECK (id=1),
        total_audio_files INTEGER DEFAULT 0,
        total_audio_duration INTEGER DEFAULT 0,
        total_audio_size INTEGER DEFAULT 0,
        users_total INTEGER DEFAULT 0,
        male_count INTEGER DEFAULT 0,
        female_count INTEGER DEFAULT 0,
        noanswer_count INTEGER DEFAULT 0,
        lang_en INTEGER DEFAULT 0,
        lang_de INTEGER DEFAULT 0,
        lang_ru INTEGER DEFAULT 0,
        lang_fr INTEGER DEFAULT 0,
        lang_zh INTEGER DEFAULT 0,
        lang_hi INTEGER DEFAULT 0,
        lang_ar INTEGER DEFAULT 0,
        age_18_29 INTEGER DEFAULT 0,
        age_30_39 INTEGER DEFAULT 0,
        age_40_49 INTEGER DEFAULT 0,
        age_50_59 INTEGER DEFAULT 0,
        age_60_69 INTEGER DEFAULT 0,
        age_70_79 INTEGER DEFAULT 0,
        age_80_89 INTEGER DEFAULT 0,
        age_90_plus INTEGER DEFAULT 0
    )""")
    c.execute("INSERT OR IGNORE INTO stats(id) VALUES (1)")
    conn.commit()


def update_stats() -> None:
    """Recalculate aggregated statistics and store them in the stats table."""
    conn = get_connection()
    c = conn.cursor()

    total_audio_files, total_audio_duration, total_audio_size = c.execute(
        "SELECT COUNT(*), COALESCE(SUM(duration),0), COALESCE(SUM(file_size),0) FROM wbmms_voice"
    ).fetchone()

    users_total = c.execute("SELECT COUNT(*) FROM user_profile").fetchone()[0]
    male_count = c.execute("SELECT COUNT(*) FROM user_profile WHERE gender='male'").fetchone()[0]
    female_count = c.execute("SELECT COUNT(*) FROM user_profile WHERE gender='female'").fetchone()[0]
    noanswer_count = users_total - male_count - female_count

    lang_counts = {l: c.execute(
        "SELECT COUNT(*) FROM user_profile WHERE language=?", (l,)
    ).fetchone()[0] for l in LANGS}

    age_counts = {}
    for label, start, end in AGE_RANGES:
        if end is None:
            age_counts[label] = c.execute(
                "SELECT COUNT(*) FROM user_profile WHERE age>=?", (start,)
            ).fetchone()[0]
        else:
            age_counts[label] = c.execute(
                "SELECT COUNT(*) FROM user_profile WHERE age BETWEEN ? AND ?",
                (start, end),
            ).fetchone()[0]

    c.execute(
        """
        UPDATE stats SET
            total_audio_files=?,
            total_audio_duration=?,
            total_audio_size=?,
            users_total=?,
            male_count=?,
            female_count=?,
            noanswer_count=?,
            lang_en=?, lang_de=?, lang_ru=?, lang_fr=?, lang_zh=?, lang_hi=?, lang_ar=?,
            age_18_29=?, age_30_39=?, age_40_49=?, age_50_59=?, age_60_69=?,
            age_70_79=?, age_80_89=?, age_90_plus=?
        WHERE id=1
        """,
        (
            total_audio_files,
            total_audio_duration,
            total_audio_size,
            users_total,
            male_count,
            female_count,
            noanswer_count,
            lang_counts.get("en", 0),
            lang_counts.get("de", 0),
            lang_counts.get("ru", 0),
            lang_counts.get("fr", 0),
            lang_counts.get("zh", 0),
            lang_counts.get("hi", 0),
            lang_counts.get("ar", 0),
            age_counts.get("18_29", 0),
            age_counts.get("30_39", 0),
            age_counts.get("40_49", 0),
            age_counts.get("50_59", 0),
            age_counts.get("60_69", 0),
            age_counts.get("70_79", 0),
            age_counts.get("80_89", 0),
            age_counts.get("90_plus", 0),
        ),
    )
    conn.commit()


def get_stats() -> dict:
    """Return aggregated statistics from the stats table."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM stats WHERE id=1").fetchone()
    return dict(row) if row else {}


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
    update_stats()


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
    update_stats()


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
    update_stats()
