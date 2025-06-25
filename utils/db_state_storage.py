from utils.db import load_session, save_session

from contextlib import contextmanager


class SqliteStateStorage:
    """Simple persistent state storage using SQLite."""

    def __init__(self):
        self._data = {}

    def get_state(self, user_id, chat_id=None, **kwargs):
        session = load_session(user_id)
        return session.get("fsm_state") if session else None

    def set_state(self, user_id, state, chat_id=None, **kwargs):
        session = load_session(user_id) or {}
        session["fsm_state"] = str(state) if state is not None else None
        save_session(user_id, session)

    def delete_state(self, user_id, chat_id=None, **kwargs):
        session = load_session(user_id) or {}
        session["fsm_state"] = None
        save_session(user_id, session)

    def get_data(self, user_id, chat_id=None, **kwargs):
        return self._data.setdefault((user_id, chat_id), {})

    @contextmanager
    def get_interactive_data(self, user_id=None, chat_id=None, **kwargs):
        data = self.get_data(user_id, chat_id)
        try:
            yield data
        finally:
            self.set_data(user_id, chat_id, data)

    def set_data(self, user_id, chat_id=None, data=None, **kwargs):
        self._data[(user_id, chat_id)] = data or {}

    def reset_data(self, user_id, chat_id=None, **kwargs):
        self._data.pop((user_id, chat_id), None)
