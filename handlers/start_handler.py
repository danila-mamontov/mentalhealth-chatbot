import os
import telebot
from states import SurveyStates

from config import RESPONSES_DIR
from utils.storage import context, get_translation
from utils.menu import main_menu, consent_menu
from utils.logger import logger


def register_handlers(bot: telebot.TeleBot):
    @bot.message_handler(commands=["start"], state="*")
    def start(message):
        user_id = message.chat.id
        user_language = message.from_user.language_code
        print(f"User {user_id} started the bot with language {user_language}")
        bot.send_message(user_id, "your language is: " + user_language)
        if user_language not in ["en","de","ru"]:
            user_language = "en"

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

            logger.log_event(user_id, "START BOT", f"New user {user_id}")
            bot.set_state(user_id, SurveyStates.consent, message.chat.id)
            bot.send_message(user_id,
                             get_translation(user_id, "welcome_message") + "\n\n" + get_translation(user_id, "consent_message"),
                             parse_mode='HTML',
                             reply_markup=consent_menu(user_id))

        else:
            logger.log_event(user_id, "START BOT", f"Existing user {user_id}")
            bot.set_state(user_id, SurveyStates.main_menu, message.chat.id)
            bot.send_message(user_id,
                             get_translation(user_id, "welcome_message") + "\n\n" + get_translation(user_id, "main_menu_message"),
                             parse_mode='HTML',
                             reply_markup=main_menu(user_id))

