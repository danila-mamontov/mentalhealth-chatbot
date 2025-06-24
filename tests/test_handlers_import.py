import importlib
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Provide a minimal stub for telebot so modules import correctly
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
sys.modules.setdefault(
    "telebot.types",
    sys.modules["telebot"].types,
)
sys.modules.setdefault(
    "telebot.handler_backends",
    sys.modules["telebot"].handler_backends,
)

sys.modules.setdefault("numpy", SimpleNamespace())
sys.modules.setdefault("pandas", SimpleNamespace())

class DummyBot:
    def callback_query_handler(self, *args, **kwargs):
        def decorator(func):
            return func
        return decorator

    def message_handler(self, *args, **kwargs):
        def decorator(func):
            return func
        return decorator

    def set_state(self, *args, **kwargs):
        pass

    def edit_message_text(self, *args, **kwargs):
        pass

    def send_message(self, *args, **kwargs):
        pass

    def delete_state(self, *args, **kwargs):
        pass

    def retrieve_data(self, *args, **kwargs):
        from contextlib import contextmanager
        @contextmanager
        def cm():
            yield {}
        return cm()

handlers = [
    'profile_handler',
    'age_handler',
    'goto_handler',
    'start_handler',
    'help_handler',
    'delete_me_handler',
    'gender_handler',
    'consent_handler',
    'language_handler',
    'treatment_handler',
    'depression_handler',
    'depressive_handler',
    'main_menu_handler',
    'phq9_survey_handler',
    'wbmms_survey_handler',
    'voice_handler',
]


def test_register_handlers():
    bot = DummyBot()
    for mod_name in handlers:
        module = importlib.import_module(f'handlers.{mod_name}')
        assert hasattr(module, 'register_handlers')
        module.register_handlers(bot)


def test_package_attributes():
    pkg = importlib.import_module('handlers')
    for mod_name in handlers:
        module = importlib.import_module(f'handlers.{mod_name}')
        assert getattr(pkg, mod_name) is module
