import sys
import types
from types import SimpleNamespace

sys.modules.setdefault("numpy", types.ModuleType("numpy"))
sys.modules.setdefault("pandas", types.ModuleType("pandas"))

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

from utils import storage
from states import SurveyStates
from handlers import (
    main_menu_handler,
    consent_handler,
    gender_handler,
    age_handler,
)


class FlowBot:
    def __init__(self):
        self.handlers = {}
        self.sent_messages = []
        self.edited_messages = []
        self.states = {}
        self.data = {}

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
        self.states[user_id] = str(state)

    def get_state(self, user_id):
        return self.states.get(user_id)

    def send_message(self, chat_id, text, parse_mode=None, reply_markup=None):
        self.sent_messages.append({
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "reply_markup": reply_markup,
        })

    def edit_message_text(self, chat_id, message_id, text, parse_mode=None, reply_markup=None):
        self.edited_messages.append({
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
            "parse_mode": parse_mode,
            "reply_markup": reply_markup,
        })

    def retrieve_data(self, user_id, chat_id):
        from contextlib import contextmanager
        @contextmanager
        def cm():
            self.data.setdefault(user_id, {})
            yield self.data[user_id]
        return cm()

    def delete_state(self, user_id):
        self.states.pop(user_id, None)


def test_full_flow(monkeypatch):
    bot = FlowBot()
    uc = storage.UserContext()
    monkeypatch.setattr(storage, "get_translation", lambda uid, key: key)

    for mod in (main_menu_handler, consent_handler, gender_handler, age_handler):
        monkeypatch.setattr(mod, "context", uc)
        monkeypatch.setattr(mod, "logger", SimpleNamespace(log_event=lambda *a, **k: None))
        monkeypatch.setattr(mod, "get_translation", lambda uid, key: key)
    monkeypatch.setattr(main_menu_handler, "consent_menu", lambda uid: "consent")
    monkeypatch.setattr(main_menu_handler, "gender_menu", lambda uid: "gender")
    monkeypatch.setattr(main_menu_handler, "age_range_menu", lambda uid: "age")
    monkeypatch.setattr(main_menu_handler, "phq9_menu", lambda idx, opts: "phq9")
    monkeypatch.setattr(consent_handler, "gender_menu", lambda uid: "gender")
    monkeypatch.setattr(consent_handler, "age_range_menu", lambda uid: "age")
    monkeypatch.setattr(consent_handler, "phq9_menu", lambda idx, opts: "phq9")
    monkeypatch.setattr(gender_handler, "age_range_menu", lambda uid: "age")
    monkeypatch.setattr(gender_handler, "phq9_menu", lambda idx, opts: "phq9")
    monkeypatch.setattr(age_handler, "phq9_menu", lambda idx, opts: "phq9")
    monkeypatch.setattr(main_menu_handler, "get_phq9_question_and_options", lambda i, uid: ("Q", [1, 2, 3, 4]))
    monkeypatch.setattr(gender_handler, "get_phq9_question_and_options", lambda i, uid: ("Q", [1, 2, 3, 4]))
    monkeypatch.setattr(consent_handler, "get_phq9_question_and_options", lambda i, uid: ("Q", [1, 2, 3, 4]))
    monkeypatch.setattr(age_handler, "get_phq9_question_and_options", lambda i, uid: ("Q", [1, 2, 3, 4]))

    main_menu_handler.register_handlers(bot)
    consent_handler.register_handlers(bot)
    gender_handler.register_handlers(bot)
    age_handler.register_handlers(bot)

    uc.add_new_user(1)

    call = SimpleNamespace(message=SimpleNamespace(chat=SimpleNamespace(id=1), message_id=10), data="menu_start_phq9_survey")
    bot.handlers["handle_menu_buttons"](call)
    assert bot.states[1] == str(SurveyStates.consent)
    assert bot.edited_messages[-1]["reply_markup"] == "consent"

    call = SimpleNamespace(message=SimpleNamespace(chat=SimpleNamespace(id=1), message_id=10), data="yes")
    bot.handlers["handle_consent"](call)
    assert bot.states[1] == str(SurveyStates.gender)
    assert bot.edited_messages[-1]["reply_markup"] == "gender"

    call = SimpleNamespace(message=SimpleNamespace(chat=SimpleNamespace(id=1), message_id=10), data="male")
    bot.handlers["handle_gender_selection"](call)
    assert bot.states[1] == str(SurveyStates.age)
    assert bot.edited_messages[-1]["reply_markup"] == "age"

    call = SimpleNamespace(message=SimpleNamespace(chat=SimpleNamespace(id=1), message_id=10), data="30")
    bot.handlers["handle_exact_age_selection"](call)
    assert bot.states[1] == str(SurveyStates.phq9)
    assert bot.edited_messages[-1]["text"] == "intro_phq9_message"
    assert bot.sent_messages[-1]["reply_markup"] == "phq9"
