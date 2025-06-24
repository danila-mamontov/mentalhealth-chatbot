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

        def delete_message(self, chat_id, message_id):
            pass

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


def test_update_controls_resends(monkeypatch):
    import importlib
    import survey_session as ss
    import handlers.wbmms_survey_handler as wsh

    importlib.reload(ss)
    importlib.reload(wsh)

    sess = ss.SurveySession(1)

    class Bot:
        def __init__(self):
            self.sent = []
            self.deleted = []

        def delete_message(self, chat_id, message_id):
            self.deleted.append(message_id)

        def send_message(self, chat_id, text, parse_mode=None, reply_markup=None):
            self.sent.append(text)
            return SimpleNamespace(message_id=len(self.sent))

    bot = Bot()
    monkeypatch.setattr(wsh, "survey_menu", lambda uid, qi: "menu")

    wsh.context.set_user_info_field(1, "survey_controls_id", None)

    wsh._update_controls(bot, sess, prefix="one")
    first_id = wsh.context.get_user_info_field(1, "survey_controls_id")
    wsh._update_controls(bot, sess, prefix="two")

    assert bot.deleted[-1] == first_id
    assert bot.sent == ["one", "two"]


def test_save_voice_answers_deletes_messages(monkeypatch):
    import importlib
    import survey_session as ss
    import handlers.wbmms_survey_handler as wsh

    importlib.reload(ss)
    importlib.reload(wsh)

    sess = ss.SurveySession(1)
    va1 = ss.VoiceAnswer(1, 0, "u1", "f1", "path1", 1, 1, 0)
    va2 = ss.VoiceAnswer(1, 0, "u2", "f2", "path2", 2, 2, 0)
    sess.record_voice(10, va1)
    sess.record_voice(11, va2)

    class Bot:
        def __init__(self):
            self.deleted = []

        def download_file(self, path):
            return b"d"

        def delete_message(self, chat_id, message_id):
            self.deleted.append(message_id)

    bot = Bot()
    wsh._save_voice_answers(bot, sess, question_index=0)

    assert set(bot.deleted) == {10, 11}
    assert va1.saved and va2.saved


def test_delete_unsaved_voice_not_persisted(tmp_path, monkeypatch):
    db_file = tmp_path / "bot.db"
    monkeypatch.setenv("DB_PATH", str(db_file))

    import config
    import utils.db as db
    import importlib
    importlib.reload(config)
    importlib.reload(db)
    db.init_db()

    import handlers.wbmms_survey_handler as wsh
    importlib.reload(wsh)

    monkeypatch.setattr(wsh, "RESPONSES_DIR", str(tmp_path / "resp"))

    import survey_session as ss
    importlib.reload(ss)

    sess = ss.SurveySession(1)
    va = ss.VoiceAnswer(1, 0, "uid", "fid", "remote", 1, 1, 0)
    sess.record_voice(5, va)

    removed = sess.delete_voice(0)
    assert removed[1] is va

    class Bot:
        def download_file(self, path):
            raise AssertionError("should not download")

    wsh._save_voice_answers(Bot(), sess, question_index=0)

    conn = db.get_connection()
    assert conn.execute("SELECT COUNT(*) FROM wbmms_voice").fetchone()[0] == 0



def test_manual_deleted_voice_not_saved(tmp_path, monkeypatch):
    db_file = tmp_path / "bot.db"
    monkeypatch.setenv("DB_PATH", str(db_file))

    import config
    import utils.db as db
    import importlib
    importlib.reload(config)
    importlib.reload(db)
    db.init_db()

    import handlers.wbmms_survey_handler as wsh
    importlib.reload(wsh)

    monkeypatch.setattr(wsh, "RESPONSES_DIR", str(tmp_path / "resp"))

    import survey_session as ss
    importlib.reload(ss)

    sess = ss.SurveySession(1)
    va = ss.VoiceAnswer(1, 0, "uid", "fid", "remote", 1, 1, 0)
    sess.record_voice(5, va)

    class Bot:
        def __init__(self):
            self.downloaded = False

        def delete_message(self, chat_id, message_id):
            raise Exception("Bad Request: message to delete not found")

        def download_file(self, path):
            self.downloaded = True
            return b"data"

    bot = Bot()
    wsh._save_voice_answers(bot, sess, question_index=0)

    assert not bot.downloaded
    assert sess.voice_messages == {}
    conn = db.get_connection()
    assert conn.execute("SELECT COUNT(*) FROM wbmms_voice").fetchone()[0] == 0


def test_manual_deleted_saved_voice_removed(tmp_path, monkeypatch):
    db_file = tmp_path / "bot.db"
    monkeypatch.setenv("DB_PATH", str(db_file))

    import config
    import utils.db as db
    import importlib
    importlib.reload(config)
    importlib.reload(db)
    db.init_db()

    import handlers.wbmms_survey_handler as wsh
    importlib.reload(wsh)

    monkeypatch.setattr(wsh, "RESPONSES_DIR", str(tmp_path / "resp"))

    import survey_session as ss
    importlib.reload(ss)

    sess = ss.SurveySession(1)
    va = ss.VoiceAnswer(1, 0, "uid", "fid", "remote", 1, 1, 0)
    sess.record_voice(5, va)
    va.saved = True
    local_dir = tmp_path / "resp" / "1" / "audio"
    os.makedirs(local_dir, exist_ok=True)
    local_path = local_dir / "old.ogg"
    local_path.write_bytes(b"data")
    va.file_path = str(local_path)
    va.file_size = len(b"data")
    db.insert_voice_metadata(1, 0, "uid", str(local_path), 1, 1, len(b"data"))

    class Bot:
        def delete_message(self, chat_id, message_id):
            raise Exception("Bad Request: message to delete not found")

        def download_file(self, path):
            raise AssertionError("should not download")

    bot = Bot()
    wsh._save_voice_answers(bot, sess, question_index=0)

    conn = db.get_connection()
    assert conn.execute("SELECT COUNT(*) FROM wbmms_voice").fetchone()[0] == 0
    assert not os.path.exists(local_path)
    assert sess.voice_messages == {}

