from telebot.handler_backends import StatesGroup, State

class SurveyStates(StatesGroup):
    language = State()
    consent = State()
    gender = State()
    age = State()
    phq9 = State()
    wbmms = State()
    main_menu = State()
