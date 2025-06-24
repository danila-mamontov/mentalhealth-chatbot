from types import SimpleNamespace
import os
import sys
import types

sys.modules.setdefault("numpy", types.ModuleType("numpy"))
sys.modules.setdefault("pandas", types.ModuleType("pandas"))

os.environ["DB_PATH"] = ":memory:"

telebot_stub = types.ModuleType("telebot")
telebot_stub.TeleBot = object
types_mod = types.ModuleType("telebot.types")
types_mod.InlineKeyboardMarkup = object
types_mod.InlineKeyboardButton = object
telebot_stub.types = types_mod
sys.modules.setdefault("telebot.types", types_mod)
handler_backends = types.ModuleType("telebot.handler_backends")
handler_backends.StatesGroup = object
handler_backends.State = object
telebot_stub.handler_backends = handler_backends
sys.modules.setdefault("telebot.handler_backends", handler_backends)
sys.modules.setdefault("telebot", telebot_stub)

from handlers import help_handler, start_handler, delete_me_handler
from utils import storage
from states import SurveyStates

class FakeBot:
    def __init__(self):
        self.handlers = {}
        self.sent_messages = []
        self.states = {}
    def message_handler(self, *args, **kwargs):
        def decorator(func):
            self.handlers[func.__name__] = func
            return func
        return decorator
    def callback_query_handler(self, *args, **kwargs):
        def decorator(func):
            self.handlers[func.__name__] = func
            return func
        return decorator
    def set_state(self, user_id, state, chat_id):
        self.states[user_id] = state
    def get_state(self, user_id):
        return self.states.get(user_id)
    def send_message(self, chat_id, text, parse_mode=None, reply_markup=None):
        self.sent_messages.append({
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "reply_markup": reply_markup,
        })
    def delete_state(self, user_id):
        self.states.pop(user_id, None)


def test_help_handler(monkeypatch):
    bot = FakeBot()
    monkeypatch.setattr(help_handler, "get_translation", lambda uid, key: f"{key}_{uid}")
    help_handler.register_handlers(bot)
    msg = SimpleNamespace(chat=SimpleNamespace(id=10))
    bot.handlers["handle_help"](msg)
    assert bot.sent_messages[0]["text"] == "help_10"


def test_start_handler_new_user(monkeypatch):
    bot = FakeBot()
    uc = storage.UserContext()
    monkeypatch.setattr(uc, "save_user_info", lambda user_id: None)
    monkeypatch.setattr(start_handler, "context", uc)
    monkeypatch.setattr(start_handler, "logger", SimpleNamespace(log_event=lambda *a, **k: None))
    monkeypatch.setattr(start_handler, "main_menu", lambda uid: "main")
    monkeypatch.setattr(start_handler, "get_translation", lambda uid, key: f"{key}_{uid}")
    monkeypatch.setattr(start_handler.os.path, "exists", lambda p: False)
    monkeypatch.setattr(start_handler.os, "makedirs", lambda p, exist_ok=False: None)
    start_handler.register_handlers(bot)
    from_user = SimpleNamespace(language_code="en", first_name="A", last_name="B", username="user")
    msg = SimpleNamespace(chat=SimpleNamespace(id=5), from_user=from_user, location=None)
    bot.handlers["start"](msg)
    assert bot.states[5] == SurveyStates.main_menu
    assert bot.sent_messages[0]["reply_markup"] == "main"


def test_delete_me_and_restart(monkeypatch):
    bot = FakeBot()
    uc = storage.UserContext()
    # patch context in handlers
    monkeypatch.setattr(start_handler, "context", uc)
    monkeypatch.setattr(delete_me_handler, "context", uc)

    # avoid filesystem interactions
    monkeypatch.setattr(start_handler.os.path, "exists", lambda p: False)
    monkeypatch.setattr(start_handler.os, "makedirs", lambda p, exist_ok=False: None)
    monkeypatch.setattr(delete_me_handler.os.path, "exists", lambda p: False)
    monkeypatch.setattr(delete_me_handler.shutil, "rmtree", lambda p: None)

    # stub logger and menus
    monkeypatch.setattr(start_handler, "logger", SimpleNamespace(log_event=lambda *a, **k: None))
    monkeypatch.setattr(delete_me_handler, "logger", SimpleNamespace(close=lambda uid: None))
    monkeypatch.setattr(start_handler, "main_menu", lambda uid: "main")
    monkeypatch.setattr(start_handler, "get_translation", lambda uid, key: f"{key}_{uid}")

    start_handler.register_handlers(bot)
    delete_me_handler.register_handlers(bot)

    from_user = SimpleNamespace(language_code="en", first_name="A", last_name="B", username="user")
    msg = SimpleNamespace(chat=SimpleNamespace(id=7), from_user=from_user, location=None)

    # initial start should treat as new user
    bot.handlers["start"](msg)
    assert uc.get_user_info(7) is not None

    # delete user data
    bot.handlers["delete_user_data"](msg)
    assert uc.get_user_info(7) is None

    # starting again should show main menu again
    bot.handlers["start"](msg)
    assert bot.sent_messages[-1]["reply_markup"] == "main"


