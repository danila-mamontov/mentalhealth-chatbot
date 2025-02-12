import os
import telebot
import pandas as pd

from config import RESPONSES_DIR
from utils.storage import context
from localization import get_translation
from handlers.wbmms_survey_handler import ask_next_main_question

def register_handlers(bot: telebot.TeleBot):
    @bot.message_handler(content_types=['voice'])
    def handle_voice_message(message):
        user_id = message.chat.id

        file_info = bot.get_file(message.voice.file_id)
        file_duration = message.voice.duration
        timestamp = message.date
        current_question = context.get_user_info_field(user_id, "current_question_index")
        file_path = os.path.join(RESPONSES_DIR, f"{user_id}", "audio",
                                 f"{user_id}_{timestamp}_{current_question}.ogg")

        with open(file_path, 'wb') as f:
            downloaded_file = bot.download_file(file_info.file_path)
            f.write(downloaded_file)
        pd.DataFrame({'user_id': [user_id],'timestamp': [timestamp], 'duration': [file_duration]}).to_csv("stats.csv", mode='a', header=False, index=False)


        context.set_user_info_field(user_id, "current_question_index", current_question + 1)
        ask_next_main_question(bot, user_id)