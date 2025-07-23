import os
import telebot
from states import SurveyStates

from config import RESPONSES_DIR
from utils.storage import context, get_translation
from utils.user_map import get_user_id
from localization import get_available_languages
from utils.menu import main_menu, consent_menu, language_menu
from utils.logger import logger


def register_handlers(bot: telebot.TeleBot):
    @bot.message_handler(commands=["start"], state="*")
    def start(message):
        telegram_id = message.chat.id
        user_id = get_user_id(telegram_id)
        user_language = message.from_user.language_code
        print(f"User {user_id} started the bot with language {user_language}")
        if user_language not in get_available_languages():
            user_language = "en"

        if not os.path.exists(os.path.join(RESPONSES_DIR, f"{user_id}")):
            os.makedirs(os.path.join(RESPONSES_DIR, str(user_id), "audio"))


        if context.get_user_info(user_id) is None:
            context.add_new_user(user_id)
            context.set_user_info_field(user_id, "language", user_language)
            context.save_user_info(user_id)

            logger.log_event(user_id, "START BOT", f"New user {user_id}")

            names = {
                "en": "English",
                "de": "Deutsch",
                "ru": "Русский",
                "fr": "Français",
                "zh": "中文",
                "hi": "हिन्दी",
                "ar": "العربية",
            }
            flags = {
                "en": "🇬🇧",
                "de": "🇩🇪",
                "ru": "🇷🇺",
                "fr": "🇫🇷",
                "zh": "🇨🇳",
                "hi": "🇮🇳",
                "ar": "🇦🇪",
            }
            lang_name = names.get(user_language, user_language)
            flag = flags.get(user_language, "🏳️")

            bot.set_state(user_id, SurveyStates.language_confirm, message.chat.id)
            bot.send_message(
                telegram_id,
                get_translation(user_id, "language_confirm").format(language=lang_name, flag=flag),
                parse_mode='HTML',
                reply_markup=consent_menu(user_id),
            )

        else:
            logger.log_event(user_id, "START BOT", f"Existing user {user_id}")
            bot.set_state(user_id, SurveyStates.main_menu, message.chat.id)
            bot.send_message(
                telegram_id,
                 get_translation(user_id, "welcome_message") + "\n\n" + get_translation(user_id, "main_menu_message"),
                 parse_mode='HTML',
                 reply_markup=main_menu(user_id))

    @bot.callback_query_handler(func=lambda call: call.data in ("yes", "no"), state=SurveyStates.language_confirm)
    def confirm_language(call):
        telegram_id = call.message.chat.id
        user_id = get_user_id(telegram_id)
        message_id = call.message.message_id
        if call.data == "yes":
            bot.set_state(user_id, SurveyStates.consent, call.message.chat.id)
            bot.edit_message_text(chat_id=telegram_id,
                                  message_id=message_id,
                                  text=get_translation(user_id, "welcome_message") + "\n\n" + get_translation(user_id, "consent_message"),
                                  parse_mode='HTML',
                                  reply_markup=consent_menu(user_id))
        else:
            bot.set_state(user_id, SurveyStates.language, call.message.chat.id)
            bot.edit_message_text(chat_id=telegram_id,
                                  message_id=message_id,
                                  text=get_translation(user_id, "language_selection"),
                                  parse_mode='HTML',
                                  reply_markup=language_menu())


