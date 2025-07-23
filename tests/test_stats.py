import os
import importlib


def test_stats_updates(tmp_path, monkeypatch):
    db_file = tmp_path / "bot.db"
    monkeypatch.setenv("DB_PATH", str(db_file))
    monkeypatch.setenv("ID_DB_PATH", ":memory:")
    import importlib
    import utils.user_map as um
    importlib.reload(um)
    um.init_user_map()

    import config
    import utils.db as db
    importlib.reload(config)
    importlib.reload(db)
    db.init_db()

    # add user and voice record
    db.upsert_user_profile({
        "user_id": 1,
        "consent": None,
        "gender": "male",
        "age": 25,
        "language": "en",
        "treatment": None,
        "depressive": None,
    })

    db.insert_voice_metadata(1, 0, "uid", "file", 5, 1, 10)

    stats = db.get_stats()
    assert stats["total_audio_files"] == 1
    assert stats["male_count"] == 1
    assert stats["lang_en"] == 1
    assert stats["age_18_29"] == 1
