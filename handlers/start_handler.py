import os
import telebot
from states import SurveyStates

from config import RESPONSES_DIR
from utils.storage import context, get_translation
from localization import get_available_languages
from utils.menu import main_menu, consent_menu, language_menu
from utils.logger import logger


def register_handlers(bot: telebot.TeleBot):
    @bot.message_handler(commands=["start"], state="*")
    def start(message):
        t_id = message.chat.id
        user_language = message.from_user.language_code
        print(f"User {t_id} started the bot with language {user_language}")
        if user_language not in get_available_languages():
            user_language = "en"

        user_info = context.get_user_info(t_id)
        new_user = False
        if user_info is None:
            context.add_new_user(t_id)
            user_info = context.get_user_info(t_id)
            context.set_user_info_field(t_id, "language", user_language)
            context.save_user_info(t_id)
            logger.log_event(t_id, "START BOT", f"New user {t_id}")
            new_user = True
        else:
            logger.log_event(t_id, "START BOT", f"Existing user {t_id}")

        uid = user_info.get("id")
        user_dir = os.path.join(RESPONSES_DIR, str(uid))
        if not os.path.exists(user_dir):
            os.makedirs(os.path.join(user_dir, "audio"))

        if new_user:
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

            bot.set_state(t_id, SurveyStates.language_confirm, message.chat.id)
            bot.send_message(
                t_id,
                get_translation(t_id, "language_confirm").format(language=lang_name, flag=flag),
                parse_mode='HTML',
                reply_markup=consent_menu(t_id),
            )
        else:
            bot.set_state(t_id, SurveyStates.main_menu, message.chat.id)
            bot.send_message(
                t_id,
                get_translation(t_id, "welcome_message") + "\n\n" + get_translation(t_id, "main_menu_message"),
                parse_mode='HTML',
                reply_markup=main_menu(t_id),
            )

    @bot.callback_query_handler(func=lambda call: call.data in ("yes", "no"), state=SurveyStates.language_confirm)
    def confirm_language(call):
        t_id = call.message.chat.id
        message_id = call.message.message_id
        if call.data == "yes":
            bot.set_state(t_id, SurveyStates.consent, call.message.chat.id)
            bot.edit_message_text(chat_id=t_id,
                                  message_id=message_id,
                                  text=get_translation(t_id, "welcome_message") + "\n\n" + get_translation(t_id, "consent_message"),
                                  parse_mode='HTML',
                                  reply_markup=consent_menu(t_id))
        else:
            bot.set_state(t_id, SurveyStates.language, call.message.chat.id)
            bot.edit_message_text(chat_id=t_id,
                                  message_id=message_id,
                                  text=get_translation(t_id, "language_selection"),
                                  parse_mode='HTML',
                                  reply_markup=language_menu())


