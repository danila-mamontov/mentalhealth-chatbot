import telebot
from debugpy.common.timestamp import current

from utils.storage import context, get_translation
from survey import get_wbmms_question, keycap_numbers
from utils.menu import survey_menu
from utils.logger import logger

def register_handlers(bot: telebot.TeleBot):
    @bot.message_handler(content_types=['voice'])
    def handle_voice_message(message):
        user_id = message.chat.id

        current_question = context.get_user_info_field(user_id, "current_question_index")

        file_path = bot.get_file(message.voice.file_id).file_path
        audio_duration = message.voice.duration
        file_unique_id = message.voice.file_unique_id

        vm_ids = context.get_user_info_field(user_id, "vm_ids")
        vm_ids[message.message_id] = {"current_question": current_question,
                                      "file_unique_id": file_unique_id,
                                      "file_path": file_path,
                                      "timestamp": message.date,
                                      "audio_duration": audio_duration}


        context.set_user_info_field(user_id, "vm_ids", vm_ids)

        logger.log_event(user_id, f"VOICE WBMMS QUESTION {current_question}", f"answer id {file_unique_id}")


        if current_question <= 9:
            keycap_number = keycap_numbers[(current_question + 1)]
        else:
            keycap_number = keycap_numbers[(current_question // 10)] + keycap_numbers[(current_question % 10 + 1)]


        try:
            bot.delete_message(user_id, context.get_user_info_field(user_id, "survey_message_id"))
        except:
            pass
        sent_message = bot.send_message(chat_id=user_id,
                         text= get_translation(user_id, "voice_recieved")+"\n\n"+f"{keycap_number}\t" + get_wbmms_question(question_id=current_question, user_id=user_id),
                         parse_mode='HTML',
                         reply_markup=survey_menu(user_id, question_index=current_question))

        context.set_user_info_field(user_id, "survey_message_id", sent_message.message_id)

        # if audio_duration < 5:
        #     bot.send_message(message.chat.id, "⚠️ Голосовое сообщение слишком короткое!")
        # else:
        #     timestamp = message.date
        #     current_question = context.get_user_info_field(user_id, "current_question_index")
        #
        #     filename = f"{user_id}_{timestamp}_{current_question}.ogg"
        #     file_path = os.path.join(RESPONSES_DIR, f"{user_id}", "audio", filename)
        #     with open(file_path, 'wb') as f:
        #         downloaded_file = bot.download_file(file_info.file_path)
        #         f.write(downloaded_file)
        #     pd.DataFrame({'user_id': [user_id],'timestamp': [timestamp], 'duration': [audio_duration]}).to_csv("stats.csv", mode='a', header=False, index=False)
        #
        #
        #     context.set_user_info_field(user_id, "current_question_index", current_question + 1)
        #     logger.log_event(user_id, f"VOICE WBMMS QUESTION {current_question}", f"answer {filename}")
        #     ask_next_main_question(bot, user_id)
