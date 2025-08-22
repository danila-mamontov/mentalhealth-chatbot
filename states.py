"""State definitions for TeleBot FSM"""

from telebot.handler_backends import StatesGroup, State

class SurveyStates(StatesGroup):
    """Conversation steps handled via TeleBot's state machine."""

    language = State()
    language_confirm = State()
    welcome = State()
    consent = State()
    gender = State()
    age = State()

    phq9 = State()
    wbmms = State()

    treatment = State()
    depressive = State()

    main_menu = State()
    final_menu = State()


class EditProfileStates(StatesGroup):
    """States used when editing existing profile information."""

    language = State()
    gender = State()
    age = State()
