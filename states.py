"""State definitions for TeleBot FSM"""

from telebot.handler_backends import StatesGroup, State

class SurveyStates(StatesGroup):
    """Conversation steps handled via TeleBot's state machine."""
    language = State()
    consent = State()
    gender = State()
    age = State()

    # States for PHQ‑9 questions
    phq9_q1 = State()
    phq9_q2 = State()
    phq9_q3 = State()
    phq9_q4 = State()
    phq9_q5 = State()
    phq9_q6 = State()
    phq9_q7 = State()
    phq9_q8 = State()

    # States for WBMMS questions (14 items)
    wbmms_q1 = State()
    wbmms_q2 = State()
    wbmms_q3 = State()
    wbmms_q4 = State()
    wbmms_q5 = State()
    wbmms_q6 = State()
    wbmms_q7 = State()
    wbmms_q8 = State()
    wbmms_q9 = State()
    wbmms_q10 = State()
    wbmms_q11 = State()
    wbmms_q12 = State()
    wbmms_q13 = State()
    wbmms_q14 = State()

    main_menu = State()
