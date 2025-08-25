from __future__ import annotations
# Avoid importing telebot.types at module import time to keep tests' stubs working.
# We'll resolve InlineKeyboardMarkup/Button lazily inside functions.
from survey import marks, WBMMS_survey, emoji_mapping
from utils.storage import get_translation
from localization import get_available_languages, get_language_name, get_language_flag


def _types():
    try:
        # Prefer telebot.types when available
        from telebot import types as t
        return t.InlineKeyboardMarkup, t.InlineKeyboardButton
    except Exception:
        try:
            from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
            return InlineKeyboardMarkup, InlineKeyboardButton
        except Exception:
            # Minimal dummies for tests that don't rely on actual markup structure
            class _Dummy:
                def __init__(self, *a, **k): pass
                def add(self, *a, **k): pass
            return _Dummy, _Dummy

def language_menu():
    InlineKeyboardMarkup, InlineKeyboardButton = _types()
    markup = InlineKeyboardMarkup(row_width=1)
    # Build buttons using localization metadata (flag + human-readable name)
    for code in get_available_languages():
        label = f"{get_language_flag(code)}  {get_language_name(code)}"
        markup.add(InlineKeyboardButton(label, callback_data=code))
    return markup

def gender_menu(t_id):
    InlineKeyboardMarkup, InlineKeyboardButton = _types()
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("♂️ " + get_translation(t_id, "male_msg"), callback_data="male"),
        InlineKeyboardButton("♀️ " + get_translation(t_id, "female_msg"), callback_data="female"),
        InlineKeyboardButton(get_translation(t_id, "noanswer_msg"), callback_data="noanswer"),
    )
    return markup


def yes_no_menu(t_id):
    InlineKeyboardMarkup, InlineKeyboardButton = _types()
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("✅ " + get_translation(t_id, "yes_msg"), callback_data="yes"),
        InlineKeyboardButton("❌ " + get_translation(t_id, "no_msg"), callback_data="no"),
        InlineKeyboardButton(get_translation(t_id, "noanswer_msg"), callback_data="noanswer"),
    )
    return markup


def age_range_menu(t_id):
    InlineKeyboardMarkup, InlineKeyboardButton = _types()
    keyboard = InlineKeyboardMarkup(row_width=3)

    age_ranges = [
        "18-29",
        "30-39",
        "40-49",
        "50-59",
        "60-69",
        "70-79",
        "80-89",
        "90+",
    ]

    buttons = [InlineKeyboardButton(text=age, callback_data=age) for age in age_ranges]
    keyboard.add(*buttons)

    return keyboard

def exact_age_menu(t_id, start, end):
    InlineKeyboardMarkup, InlineKeyboardButton = _types()
    keyboard = InlineKeyboardMarkup(row_width=3)

    buttons = [InlineKeyboardButton(text=str(age), callback_data=str(age)) for age in range(start, end + 1)]
    keyboard.add(*buttons)

    keyboard.add(InlineKeyboardButton(marks[1]+"\t"+get_translation(t_id, "back_msg"), callback_data="goto_age_range"))

    return keyboard

# Main menu
def main_menu(t_id):
    InlineKeyboardMarkup, InlineKeyboardButton = _types()
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
                InlineKeyboardButton(get_translation(t_id, 'phq9_survey_button_msg'), callback_data="menu_start_phq9_survey"),
                InlineKeyboardButton(get_translation(t_id, "open_profile_button_msg"), callback_data="profile_open"),
                # InlineKeyboardButton(get_translation(t_id,'main_survey_button_msg'), callback_data="menu_start_main_survey"),
                InlineKeyboardButton(url="http://health-bot.dialogue-systems.org/", text=get_translation(t_id, "website_msg")),
               InlineKeyboardButton(text=get_translation(t_id,"share_bot_button_msg"),switch_inline_query=get_translation(t_id,"share_bot_text_msg"))
               )

    return markup

def final_menu(t_id):
    InlineKeyboardMarkup, InlineKeyboardButton = _types()
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(url="http://health-bot.dialogue-systems.org/", text=get_translation(t_id, "website_msg")),
        InlineKeyboardButton(text=get_translation(t_id,"share_bot_button_msg"),switch_inline_query=get_translation(t_id,"share_bot_text_msg"))
    )
    return markup

def consent_menu(t_id):
    InlineKeyboardMarkup, InlineKeyboardButton = _types()
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(
            "✅ " + get_translation(t_id, "yes_msg"), callback_data="yes"
        ),
        InlineKeyboardButton(
            "❌ " + get_translation(t_id, "no_msg"), callback_data="no"
        ),
    )
    return markup

def survey_menu(t_id, question_index: int, voice_count: int = 0):
    InlineKeyboardMarkup, InlineKeyboardButton = _types()
    if question_index == 0:
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton(
                marks[2] + "\t" + get_translation(t_id, "next_msg"), callback_data="survey_next"
            )
        )
    elif question_index < len(WBMMS_survey["en"]) - 1:
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton(
                marks[1] + "\t" + get_translation(t_id, "back_msg"), callback_data="survey_prev"
            ),
            InlineKeyboardButton(
                marks[2] + "\t" + get_translation(t_id, "next_msg"), callback_data="survey_next"
            ),
        )
    else:
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton(
                marks[1] + "\t" + get_translation(t_id, "back_msg"), callback_data="survey_prev"
            ),
            InlineKeyboardButton(
                marks[0] + "\t" + get_translation(t_id, "finish_button_msg"), callback_data="survey_finish"
            ),
        )
    return markup

def profile_menu(t_id):
    InlineKeyboardMarkup, InlineKeyboardButton = _types()
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(get_translation(t_id, "change_language_button_msg"),
                                    callback_data="set_language_change"),
               InlineKeyboardButton(get_translation(t_id, "change_gender_button_msg"),
                                    callback_data="set_gender_change"),
                InlineKeyboardButton(get_translation(t_id, "change_age_button_msg"),
                                     callback_data="range_change"),
                InlineKeyboardButton(get_translation(t_id, "back_msg"), callback_data="goto_main_menu"))
    return markup

def phq9_menu(index ,options):
    InlineKeyboardMarkup, InlineKeyboardButton = _types()
    markup = InlineKeyboardMarkup(row_width=1)
    for i, option in enumerate(options):
        markup.add(InlineKeyboardButton(emoji_mapping[i + 1] + '\t' + option, callback_data=f"answer_{index}_{i}"))

    return markup
