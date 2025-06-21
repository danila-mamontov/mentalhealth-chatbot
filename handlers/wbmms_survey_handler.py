import telebot
import os
import pandas as pd
from telebot.types import CallbackQuery
from utils.menu import survey_menu, main_menu
from survey import keycap_numbers
from survey import get_wbmms_question, WBMMS_survey
from utils.storage import context, get_translation
from utils.logger import logger
from config import RESPONSES_DIR
from states import SurveyStates

def save_wbmms_answer(bot, message, user_id):
    vm_ids = context.get_user_info_field(user_id, "vm_ids")
    for vm_id in vm_ids:
        audio_question_id = vm_ids[vm_id]["current_question"]
        audio_unique_id = vm_ids[vm_id]["file_unique_id"]
        audio_file_path = vm_ids[vm_id]["file_path"]
        timestamp = vm_ids[vm_id]["timestamp"]
        audio_duration = vm_ids[vm_id]["audio_duration"]

        filename_to_save = f"{user_id}_{timestamp}_{audio_question_id}.ogg"
        file_path_to_save = os.path.join(RESPONSES_DIR, f"{user_id}", "audio", filename_to_save)
        with open(file_path_to_save, 'wb') as f:
            downloaded_file = bot.download_file(audio_file_path)
            f.write(downloaded_file)
        pd.DataFrame({'user_id': [user_id],'audio_unique_id': [audio_unique_id], 'duration': [audio_duration]}).to_csv("stats.csv",
                                                                                                            mode='a',
                                                                                                            header=False,
                                                                                                            index=False)


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
    @bot.callback_query_handler(func=lambda call: call.data.startswith("go_to_question_"), state=SurveyStates.wbmms)
    def handle_control_button(call: CallbackQuery):
        user_id = call.message.chat.id
        message_id = call.message.message_id
        respond = call.data.split("_")[-1]


        if respond != "finish":
            next_question_index = int(respond)
            save_wbmms_answer(bot, call.message, user_id)

            if next_question_index <= 9:
                keycap_number = keycap_numbers[(next_question_index + 1)]
            else:
                keycap_number = keycap_numbers[(next_question_index // 10)] + keycap_numbers[(next_question_index % 10 + 1)]

            for vm_id in context.get_user_info_field(user_id, "vm_ids"):
                try:
                    bot.delete_message(user_id, vm_id)
                except:
                    pass

            logger.log_event(user_id, "WBMMS GO TO QUESTION", next_question_index)
            context.set_user_info_field(user_id, "current_question_index", next_question_index)
            context.set_user_info_field(user_id, "vm_ids", dict())
            bot.edit_message_text(
                chat_id=user_id,
                message_id=message_id,
                text=f"{keycap_number}\t" + get_wbmms_question(next_question_index, user_id=user_id),
                parse_mode='HTML',
                reply_markup=survey_menu(user_id, next_question_index)
            )
        elif respond == "finish":
            save_wbmms_answer(bot, call.message, user_id)
            try:
                bot.delete_message(user_id, context.get_user_info_field(user_id, "message_to_del"))
            except:
                pass
            for vm_id in context.get_user_info_field(user_id, "vm_ids"):
                bot.delete_message(user_id, vm_id)

            context.set_user_info_field(user_id, "current_question_index", 0)
            context.set_user_info_field(user_id, "vm_ids", dict())
            logger.log_event(user_id, "END WBMMS SURVEY")
            bot.edit_message_text(chat_id=user_id,
                                  message_id=call.message.message_id,
                                  text=get_translation(user_id, "end_phq9_message") + "\n\n" + get_translation(user_id,
                                                                                                               'main_menu_message'),
                                  parse_mode='HTML',
                                  reply_markup=main_menu(user_id))
            bot.set_state(user_id, SurveyStates.main_menu, call.message.chat.id)
        else:
            logger.log_event(user_id, "WBMMS GO TO QUESTION", "ERROR")
            bot.send_message(user_id, get_translation(user_id, "error_message"))
            bot.send_message(user_id, get_translation(user_id, "end_main_survey_message"))

