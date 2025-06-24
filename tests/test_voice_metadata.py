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

    import survey_session as ss
    importlib.reload(ss)

    sess = ss.SurveyManager.get_session(1)
    va = ss.VoiceAnswer(
        user_id=1,
        question_id=3,
        file_unique_id="uid123",
        file_id="id123",
        file_path="server_path",
        duration=7,
        timestamp=111,
        file_size=0,
    )
    sess.record_voice(10, va)

    class FakeBot:
        def download_file(self, path):
            assert path == "server_path"
            return b"data"

    wsh._save_voice_answers(FakeBot(), sess)

    assert va.saved
    assert va.file_size == 4

    conn = db.get_connection()
    row = conn.execute("SELECT * FROM wbmms_voice").fetchone()

    assert row["user_id"] == 1
    assert row["question_id"] == 3
    assert row["file_unique_id"] == "uid123"
    assert row["duration"] == 7
    assert row["timestamp"] == 111
    assert os.path.exists(row["file_path"])
    assert row["file_size"] == 4


def test_render_question_handles_not_modified(monkeypatch):
    import importlib
    import survey_session as ss
    import handlers.wbmms_survey_handler as wsh

    importlib.reload(ss)
    importlib.reload(wsh)

    sess = ss.SurveySession(1)
    va1 = ss.VoiceAnswer(1, 0, "u1", "f1", "path", 1, 1, 0)
    va2 = ss.VoiceAnswer(1, 0, "u2", "f2", "path", 1, 2, 0)
    sess.record_voice(10, va1)
    sess.record_voice(11, va2)

    class Bot:
        def __init__(self):
            self.sent = []

        def edit_message_text(self, **kwargs):
            raise Exception("Bad Request: message is not modified")

        def delete_message(self, chat_id, message_id):
            pass

        def send_voice(self, chat_id, file_id):
            self.sent.append(file_id)
            return SimpleNamespace(message_id=len(self.sent))

        def send_message(self, chat_id, text, parse_mode=None, reply_markup=None):
            return SimpleNamespace(message_id=99)

    bot = Bot()
    monkeypatch.setattr(wsh, "get_wbmms_question", lambda *a, **k: "Q")
    monkeypatch.setattr(wsh, "survey_menu", lambda uid, qi: "menu")
    monkeypatch.setattr(wsh, "get_translation", lambda uid, key: "txt")

    wsh._render_question(bot, sess, 99, prefix="msg")
    assert bot.sent == ["f1", "f2"]

