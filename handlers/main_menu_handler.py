import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from localization import get_translation
from survey import get_wbmms_question,get_phq9_question_and_options, keycap_numbers
from utils.menu import survey_menu, phq9_menu
from utils.storage import context
from utils.logger import logger

def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("menu_"))
    def handle_menu_buttons(call):
        user_id = call.message.chat.id
        message_id = call.message.message_id
        if call.data == "menu_start_phq9_survey":
            context.set_user_info_field(user_id, "current_question_index", 0)
            question, options = get_phq9_question_and_options(0, user_id)

            context.set_user_info_field(user_id, "message_to_del", message_id)

            logger.log_event(user_id, "START PHQ9 SURVEY")
            bot.edit_message_text(chat_id=user_id,
                                  message_id=message_id,
                                  text=get_translation(user_id, 'intro_phq9_message'),
                                  parse_mode='HTML')

            bot.send_message(chat_id=user_id,
                             text=get_translation(user_id, 'starting_phq9')+f"\n{keycap_numbers[1]}\t"+f"<i><b>{question}</b></i>",
                             parse_mode='HTML',
                             reply_markup=phq9_menu(0, options))

            # ask_phq9_question(bot, user_id)
        elif call.data == "menu_start_main_survey":
            context.set_user_info_field(user_id, "current_question_index", 0)
            context.set_user_info_field(user_id, "message_to_del", message_id)

            logger.log_event(user_id, "START WBMMS SURVEY")
            bot.edit_message_text(chat_id=user_id,
                                  message_id=message_id,
                                  text=get_translation(user_id, 'intro_main_message'),
                                  parse_mode='HTML')
            bot.send_message(chat_id=user_id,
                             text=f"{keycap_numbers[1]}\t"+ get_wbmms_question(question_id=0,user_id=user_id),
                             parse_mode='HTML',
                             reply_markup=survey_menu(user_id, question_index=0))

        else:
            bot.send_message(user_id, "Invalid option selected.")
