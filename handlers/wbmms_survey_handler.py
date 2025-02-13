import telebot
from telebot.types import CallbackQuery
from utils.menu import survey_menu, main_menu
from localization import get_translation
from survey import keycap_numbers
from survey import get_wbmms_question, WBMMS_survey
from utils.storage import context
from utils.logger import logger

def ask_next_main_question(bot, user_id):
    language = context.get_user_info_field(user_id, "language")
    index = context.get_user_info_field(user_id, "current_question_index")

    if index < len(WBMMS_survey["en"]):
        if index <= 9:
            keycap_number = keycap_numbers[(index+1)]
        else:
            keycap_number = keycap_numbers[(index//10)]+keycap_numbers[(index%10+1)]

        bot.send_message(user_id, f"{keycap_number}\t"+ get_wbmms_question(index, language=language), parse_mode='HTML')
    else:
        bot.send_message(user_id, get_translation(language, "end_main_survey_message"))
        bot.send_message(user_id, get_translation(language, "main_menu_message"), reply_markup=main_menu(user_id))

def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("go_to_question_"))
    def handle_control_button(call: CallbackQuery):
        user_id = call.message.chat.id
        message_id = call.message.message_id
        respond = call.data.split("_")[-1]

        if respond != "finish":
            question_index = int(respond)

            if question_index <= 9:
                keycap_number = keycap_numbers[(question_index + 1)]
            else:
                keycap_number = keycap_numbers[(question_index // 10)] + keycap_numbers[(question_index % 10 + 1)]

            logger.log_event(user_id, "WBMMS GO TO QUESTION", question_index)
            bot.edit_message_text(
                chat_id=user_id,
                message_id=message_id,
                text=f"{keycap_number}\t" + get_wbmms_question(question_index, user_id=user_id),
                parse_mode='HTML',
                reply_markup=survey_menu(user_id, question_index)
            )
        elif respond == "finish":
            context.set_user_info_field(user_id, "current_question_index", 0)

            logger.log_event(user_id, "END WBMMS SURVEY")
            bot.delete_message(user_id, context.get_user_info_field(user_id, "message_to_del"))
            bot.edit_message_text(chat_id=user_id,
                                  message_id=call.message.message_id,
                                  text=get_translation(user_id, "end_phq9_message") + "\n\n" + get_translation(user_id,
                                                                                                               'main_menu_message'),
                                  parse_mode='HTML',
                                  reply_markup=main_menu(user_id))
        else:
            logger.log_event(user_id, "WBMMS GO TO QUESTION", "ERROR")
            bot.send_message(user_id, get_translation(user_id, "error_message"))
            bot.send_message(user_id, get_translation(user_id, "end_main_survey_message"))
