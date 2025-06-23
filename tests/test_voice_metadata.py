import os
import sys
import types
import importlib
from types import SimpleNamespace

# Stub telebot so imports in handlers succeed
sys.modules.setdefault(
    "telebot",
    SimpleNamespace(
        TeleBot=object,
        types=SimpleNamespace(
            Message=object,
            CallbackQuery=object,
            InlineKeyboardMarkup=object,
            InlineKeyboardButton=object,
        ),
        handler_backends=SimpleNamespace(StatesGroup=object, State=object),
    ),
)
sys.modules.setdefault("telebot.types", sys.modules["telebot"].types)
sys.modules.setdefault("telebot.handler_backends", sys.modules["telebot"].handler_backends)


def test_save_wbmms_answer_saves_metadata(tmp_path, monkeypatch):
    db_file = tmp_path / "bot.db"
    monkeypatch.setenv("DB_PATH", str(db_file))

    import config
    import utils.db as db
    importlib.reload(config)
    importlib.reload(db)
    db.init_db()

    import handlers.wbmms_survey_handler as wsh
    importlib.reload(wsh)

    responses_dir = tmp_path / "responses"
    os.makedirs(responses_dir / "1" / "audio", exist_ok=True)
    monkeypatch.setattr(wsh, "RESPONSES_DIR", str(responses_dir))

    class DummyContext:
        def __init__(self):
            self.data = {1: {"vm_ids": {}}}
        def get_user_info_field(self, user_id, field):
            return self.data[user_id][field]
        def set_user_info_field(self, user_id, field, value):
            self.data[user_id][field] = value

    ctx = DummyContext()
    ctx.data[1]["vm_ids"] = {
        10: {
            "current_question": 3,
            "file_unique_id": "uid123",
            "file_path": "server_path",
            "timestamp": 111,
            "audio_duration": 7,
        }
    }
    monkeypatch.setattr(wsh, "context", ctx)

    class FakeBot:
        def download_file(self, path):
            assert path == "server_path"
            return b"data"

    wsh.save_wbmms_answer(FakeBot(), None, 1)

    conn = db.get_connection()
    row = conn.execute("SELECT * FROM wbmms_voice").fetchone()

    assert row["user_id"] == 1
    assert row["question_id"] == 3
    assert row["file_unique_id"] == "uid123"
    assert row["duration"] == 7
    assert row["timestamp"] == 111
    assert os.path.exists(row["file_path"])
    assert row["file_size"] == 4

