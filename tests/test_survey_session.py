import importlib
import os

import survey_session as ss


def test_survey_manager_singleton():
    sess1 = ss.SurveyManager.get_session(1)
    sess2 = ss.SurveyManager.get_session(1)
    assert sess1 is sess2
    sess3 = ss.SurveyManager.get_session(2)
    assert sess3 is not sess1


def test_record_voice_multiple():
    sess = ss.SurveySession(1)
    va1 = ss.VoiceAnswer(1, 0, "uid1", "id1", "path1", 1, 10, 0)
    va2 = ss.VoiceAnswer(1, 0, "uid2", "id2", "path2", 2, 11, 0)

    sess.record_voice(5, va1)
    sess.record_voice(6, va2)

    assert sess.question_voice_ids[0] == [5, 6]
    assert sess.voice_messages[5] is va1
    assert sess.voice_messages[6] is va2



def test_question_navigation():
    sess = ss.SurveySession(1)

    assert sess.current_index == 0
    assert sess.next_question() == 1
    assert sess.current_index == 1
    assert sess.next_question() == 2
    assert sess.prev_question() == 1
    assert sess.prev_question() == 0
    assert sess.prev_question() == 0  # cannot go below zero
    assert sess.jump_to(3) == 3
    assert sess.current_index == 3


def test_save_voice_answers_persists(tmp_path, monkeypatch):
    db_file = tmp_path / "bot.db"
    monkeypatch.setenv("DB_PATH", str(db_file))
    import utils.db as db
    import config
    importlib.reload(config)
    importlib.reload(db)
    db.init_db()

    import handlers.wbmms_survey_handler as wsh
    importlib.reload(wsh)

    monkeypatch.setattr(wsh, "RESPONSES_DIR", str(tmp_path / "resp"))

    importlib.reload(ss)

    sess = ss.SurveyManager.get_session(1)
    va = ss.VoiceAnswer(
        user_id=1,
        question_id=2,
        file_unique_id="uid",
        file_id="id",
        file_path="server",  # remote path
        duration=3,
        timestamp=111,
        file_size=0,
    )
    sess.record_voice(10, va)

    conn = db.get_connection()
    assert conn.execute("SELECT COUNT(*) FROM wbmms_voice").fetchone()[0] == 0

    class Bot:
        def download_file(self, path):
            assert path == "server"
            return b"data"

        def delete_message(self, chat_id, message_id):
            pass

    wsh._save_voice_answers(Bot(), sess)

    assert va.saved
    assert va.file_size == 4

    row = conn.execute("SELECT * FROM wbmms_voice").fetchone()
    assert row["user_id"] == 1
    assert row["question_id"] == 2
    assert row["file_unique_id"] == "uid"
    assert row["duration"] == 3
    assert row["timestamp"] == 111
    assert os.path.exists(row["file_path"])
    assert row["file_size"] == 4
