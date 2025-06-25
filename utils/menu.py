from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from survey import marks, WBMMS_survey, emoji_mapping
from utils.storage import get_translation


def language_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("English", callback_data="en"),
        InlineKeyboardButton("Deutsch", callback_data="de"),
        InlineKeyboardButton("Русский", callback_data="ru"),
    )
    return markup

def gender_menu(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("♂️ " + get_translation(user_id, "male"), callback_data="male"),
        InlineKeyboardButton("♀️ " + get_translation(user_id, "female"), callback_data="female"),
        InlineKeyboardButton(get_translation(user_id, "noanswer"), callback_data="noanswer"),
    )
    return markup

def depression_diagnosis_menu(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("✅ " + get_translation(user_id, "yes"), callback_data="yes"),
        InlineKeyboardButton("❌ " + get_translation(user_id, "no"), callback_data="no"),
        InlineKeyboardButton(get_translation(user_id, "no_answer"), callback_data="noanswer"),
    )

def depressive_menu(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("✅ " + get_translation(user_id, "yes"), callback_data="yes"),
        InlineKeyboardButton("❌ " + get_translation(user_id, "no"), callback_data="no"),
        InlineKeyboardButton(get_translation(user_id, "no_answer"), callback_data="noanswer"),
    )
    return markup

def treatment_menu(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("✅ " + get_translation(user_id, "yes"), callback_data="yes"),
        InlineKeyboardButton("❌ " + get_translation(user_id, "no"), callback_data="no"),
        InlineKeyboardButton(get_translation(user_id, "no_answer"), callback_data="noanswer"),
    )
    return markup

def age_range_menu(user_id):
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

def exact_age_menu(user_id, start, end):
    keyboard = InlineKeyboardMarkup(row_width=3)

    buttons = [InlineKeyboardButton(text=str(age), callback_data=str(age)) for age in range(start, end + 1)]
    keyboard.add(*buttons)

    # Кнопка "Назад"
    keyboard.add(InlineKeyboardButton(marks[1]+"\t"+get_translation(user_id, "back"), callback_data="goto_age_range"))

    return keyboard

# Main menu
def main_menu(user_id):

    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
                InlineKeyboardButton(get_translation(user_id, 'phq9_survey_button'), callback_data="menu_start_phq9_survey"),
                InlineKeyboardButton(get_translation(user_id, "open_profile_button"), callback_data="profile_open"),
                # InlineKeyboardButton(get_translation(user_id,'main_survey_button'), callback_data="menu_start_main_survey"),
                InlineKeyboardButton(url="http://huskey.e-technik.uni-ulm.de", text=get_translation(user_id, "website")),
               InlineKeyboardButton(text=get_translation(user_id,"share_bot_button"),switch_inline_query=get_translation(user_id,"share_bot_text"))
               )

    return markup

def consent_menu(user_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(
            "✅ " + get_translation(user_id, "yes"), callback_data="yes"
        ),
        InlineKeyboardButton(
            "❌ " + get_translation(user_id, "no"), callback_data="no"
        ),
    )
    return markup

def survey_menu(user_id, question_index: int, voice_count: int = 0):
    if question_index == 0:
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton(
                marks[2] + "\t" + get_translation(user_id, "next"), callback_data="survey_next"
            )
        )
    elif question_index < len(WBMMS_survey["en"]) - 1:
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton(
                marks[1] + "\t" + get_translation(user_id, "back"), callback_data="survey_prev"
            ),
            InlineKeyboardButton(
                marks[2] + "\t" + get_translation(user_id, "next"), callback_data="survey_next"
            ),
        )
    else:
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton(
                marks[1] + "\t" + get_translation(user_id, "back"), callback_data="survey_prev"
            ),
            InlineKeyboardButton(
                marks[0] + "\t" + get_translation(user_id, "finish_button"), callback_data="survey_finish"
            ),
        )
    return markup

def profile_menu(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(get_translation(user_id, "change_language_button"),
                                    callback_data="set_language_change"),
               InlineKeyboardButton(get_translation(user_id, "change_gender_button"),
                                    callback_data="set_gender_change"),
                InlineKeyboardButton(get_translation(user_id, "change_age_button"),
                                     callback_data="range_change"),
                # InlineKeyboardButton(get_translation(user_id, "change_depression_diagnosis"), callback_data="change_depression_diagnosis"),
                # InlineKeyboardButton(get_translation(user_id, "change_depressive"), callback_data="change_depressive"),
                # InlineKeyboardButton(get_translation(user_id, "change_treatment"), callback_data="change_treatment"),
                InlineKeyboardButton(get_translation(user_id, "back"), callback_data="goto_main_menu"))
    return markup

def phq9_menu(index ,options):
    markup = InlineKeyboardMarkup(row_width=1)
    for i, option in enumerate(options):
        markup.add(InlineKeyboardButton(emoji_mapping[i + 1] + '\t' + option, callback_data=f"answer_{index}_{i}"))

    return markup
