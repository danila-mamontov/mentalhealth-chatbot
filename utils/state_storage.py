from __future__ import annotations

from telebot.storage import StateStorageBase
from telebot.storage.base_storage import StateContext
from .db import load_session, save_session


class SQLiteStateStorage(StateStorageBase):
    """State storage backed by the ``user_session`` table."""

    def set_state(self, chat_id, user_id, state):
        if hasattr(state, "name"):
            state = state.name
        session = load_session(user_id) or {}
        session["fsm_state"] = state
        save_session(user_id, session)
        return True

    def delete_state(self, chat_id, user_id):
        session = load_session(user_id)
        if session is None:
            return False
        session["fsm_state"] = None
        session["state_data"] = {}
        save_session(user_id, session)
        return True

    def get_state(self, chat_id, user_id):
        session = load_session(user_id)
        return session.get("fsm_state") if session else None

    def get_data(self, chat_id, user_id):
        session = load_session(user_id)
        if session:
            return session.get("state_data") or {}
        return None

    def reset_data(self, chat_id, user_id):
        session = load_session(user_id)
        if session is None:
            return False
        session["state_data"] = {}
        save_session(user_id, session)
        return True

    def set_data(self, chat_id, user_id, key, value):
        session = load_session(user_id) or {}
        data = session.get("state_data") or {}
        data[key] = value
        session["state_data"] = data
        save_session(user_id, session)
        return True

    def get_interactive_data(self, chat_id, user_id):
        return StateContext(self, chat_id, user_id)

    def save(self, chat_id, user_id, data):
        session = load_session(user_id) or {}
        session["state_data"] = data
        save_session(user_id, session)
