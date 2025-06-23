import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import db


def test_init_db(tmp_path, monkeypatch):
    test_db = tmp_path / "test.db"
    monkeypatch.setenv("DB_PATH", str(test_db))
    db.init_db()
    conn = db.get_connection()
    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cur.fetchall()}
    conn.close()
    assert {'users', 'phq_answers', 'voice_metadata', 'logs'} <= tables
