import os
import telebot
from pyarrow.pandas_compat import dataframe_to_types

from config import RESPONSES_DIR
from utils.storage import context
from utils.menu import language_menu, main_menu, consent_menu
from utils.logger import logger
from localization import get_translation
import pandas as pd

def register_handlers(bot: telebot.TeleBot):
    @bot.message_handler(commands=["start"])
    def start(message):
        user_id = message.chat.id
        user_language = message.from_user.language_code

        if not os.path.exists(os.path.join(RESPONSES_DIR, f"{user_id}")):
            os.makedirs(os.path.join(RESPONSES_DIR, str(user_id), "audio"))


        if context.get_user_info(user_id) is None:
            context.add_new_user(user_id)
            context.set_user_info_field(user_id, "language", user_language)
            context.set_user_info_field(user_id, "first_name",message.from_user.first_name)
            context.set_user_info_field(user_id, "family_name", message.from_user.last_name)
            context.set_user_info_field(user_id, "username", message.from_user.username if message.from_user.username is not None else None)
            context.set_user_info_field(user_id, "latitude", message.location.latitude if message.location is not None else None)
            context.set_user_info_field(user_id, "longitude", message.location.longitude if message.location is not None else None)
            context.save_user_info(user_id)

            logger.log_event(user_id, "START", f"New user")
            # Send language selection menu
            # bot.send_message(user_id, 'Please choose your language:', reply_markup=language_menu())
            bot.send_message(user_id, get_translation(user_id, "welcome_message"), parse_mode='HTML')
            bot.send_message(user_id, get_translation(user_id, "consent_message"), reply_markup=consent_menu(user_id))

        else:
            logger.log_event(user_id, "START", f"Existing user")
            bot.send_message(user_id, get_translation(user_id,"welcome_message"), parse_mode='HTML')
            bot.send_message(user_id, get_translation(user_id, "main_menu_message"), reply_markup=main_menu(user_id))
