import telebot
from telebot.types import Message

from config import ADMIN_REENROLL_TOKEN
from flow.renderer import render_node, engine
from utils.menu import consent_menu
from utils.storage import context
from localization import (
    get_available_languages,
    get_language_name,
    get_language_flag,
    normalize_language,
)
from utils.logger import logger

_AVAILABLE_LANGS = get_available_languages()


def register_handlers(bot: telebot.TeleBot):
    @bot.message_handler(commands=["newparticipant"])
    def new_participant(message: Message):
        raw = (message.text or "").strip()
        parts = raw.split(maxsplit=1)
        token = parts[1].strip() if len(parts) > 1 else ""

        if not ADMIN_REENROLL_TOKEN or token != ADMIN_REENROLL_TOKEN:
            bot.reply_to(message, "Command is unavailable.")
            return

        t_id = message.chat.id
        # Always use Russian (ru) language for all users
        t_language_code = "ru"

        uid = context.reenroll_user(t_id)
        if uid is None:
            bot.reply_to(message, "Failed to start a new participant session.")
            return

        bot.delete_state(user_id=message.from_user.id, chat_id=t_id)

        # Always set language to Russian
        context.set_user_info_field(t_id, "language", t_language_code)
        context.save_user_info(t_id)

        # Re-run the onboarding flow, skip language selection
        welcome_mid = render_node(bot, t_id, engine.start)
        if welcome_mid is not None:
            context.set_user_info_field(t_id, "welcome_message_id", welcome_mid)

        # Go directly to consent (skip language_confirm)
        render_node(
            bot,
            t_id,
            "consent",
            menu=consent_menu,
        )
        logger.log_event(t_id, "REENROLL_AUTO_RU", f"New participant id={uid}")
