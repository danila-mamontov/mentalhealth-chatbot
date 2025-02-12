from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from localization import get_translation
from survey import marks, WBMMS_survey, emoji_mapping


def language_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("Continue in English", callback_data="set_language_en"),
               InlineKeyboardButton("Weiter auf Deutsch", callback_data="set_language_de"),
               InlineKeyboardButton("Продолжить на Русском", callback_data="set_language_ru"))
    return markup

def gender_menu(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("♂️ "+get_translation(user_id, "gender_male"), callback_data="set_gender_male"),
               InlineKeyboardButton("♀️ "+get_translation(user_id, "gender_female"), callback_data="set_gender_female"),
               InlineKeyboardButton(get_translation(user_id, "gender_other"), callback_data="set_gender_other"))
    return markup

def age_range_menu(user_id):
    keyboard = InlineKeyboardMarkup(row_width=3)

    age_ranges = [
        "10-19", "20-29", "30-39",
        "40-49", "50-59", "60-69",
        "70-79", "80-89", "90+"
    ]

    buttons = [InlineKeyboardButton(text=age, callback_data=f"range_{age}") for age in age_ranges]
    keyboard.add(*buttons)

    return keyboard

def exact_age_menu(user_id, start, end):
    keyboard = InlineKeyboardMarkup(row_width=3)

    buttons = [InlineKeyboardButton(text=str(age), callback_data=f"age_{age}") for age in range(start, end + 1)]
    keyboard.add(*buttons)

    # Кнопка "Назад"
    keyboard.add(InlineKeyboardButton(marks[1]+"\t"+get_translation(user_id, "previous"), callback_data="back_to_age_selection"))

    return keyboard

# Main menu
def main_menu(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(url="https://www.who.int/en/news-room/fact-sheets/detail/depression", text=get_translation(user_id, "who_website")),
                InlineKeyboardButton(get_translation(user_id, 'phq9_survey_button'), callback_data="menu_start_phq9_survey"),
                InlineKeyboardButton(get_translation(user_id,'main_survey_button'), callback_data="menu_start_main_survey"))
    return markup

def consent_menu(user_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("✅ "+get_translation(user_id,"yes"), callback_data="consent_yes"),
               InlineKeyboardButton("❌ "+get_translation(user_id, "no"), callback_data="consent_no"))
    return markup

def survey_menu(user_id, question_index : int):

    previous_button = InlineKeyboardButton(marks[1]+"\t"+get_translation(user_id, "previous"), callback_data="go_to_question_"+str(question_index-1))
    next_button     = InlineKeyboardButton(marks[2]+"\t"+get_translation(user_id, "next"), callback_data="go_to_question_"+str(question_index+1))
    if question_index == 0:
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(next_button)
    elif question_index < len(WBMMS_survey["en"])-1:
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(previous_button, next_button)
    else:
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton(marks[0]+"\t"+get_translation(user_id, "finish_button"), callback_data="go_to_question_finish"))

    return markup

def phq9_menu(index ,options):
    markup = InlineKeyboardMarkup(row_width=1)

    for i, option in enumerate(options):
        markup.add(InlineKeyboardButton(emoji_mapping[i + 1] + '\t' + option, callback_data=f"answer_{index}_{i}"))

    return markup
