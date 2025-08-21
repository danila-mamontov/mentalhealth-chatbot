from pathlib import Path
import telebot
from telebot.types import Message, CallbackQuery

from states import SurveyStates
from config import RESPONSES_DIR
from utils.storage import context, get_translation
from localization import (
    get_available_languages,
    get_language_name,
    get_language_flag,
    normalize_language,
    FALLBACK_LANGUAGE,
)
from utils.menu import main_menu, consent_menu, language_menu
from utils.logger import logger

_AVAILABLE_LANGS = get_available_languages()


def _ensure_user_dir(user_id: int) -> Path:
    base = Path(RESPONSES_DIR) / str(user_id)
    audio_dir = base / "audio"
    # exist_ok avoids race condition on simultaneous /start
    audio_dir.mkdir(parents=True, exist_ok=True)
    return base


def _needs_initial_setup(info: dict) -> bool:
    return not all(
        [
            info.get("consent"),
            info.get("language"),
            info.get("gender"),
            info.get("age"),
        ]
    )


def _safe_translation(user_id: int, key: str) -> str:
    try:
        return get_translation(user_id, key)
    except Exception as exc:  # Broad, but we want resilience in handlers
        logger.log_event(user_id, "TRANSLATION_ERROR", f"{key}: {exc}")
        return key  # Fallback to key to avoid crashing


def register_handlers(bot: telebot.TeleBot):
    @bot.message_handler(commands=["start"], state="*")
    def start(message: Message):
        t_id = message.chat.id
        t_language_code = normalize_language(getattr(message.from_user, "language_code", None), _AVAILABLE_LANGS)
        user_info = context.get_user_info(t_id)

        if user_info is None:
            context.add_new_user(t_id)
            user_info = context.get_user_info(t_id)
            logger.log_event(t_id, "START BOT", f"New user {t_id}")
        else:
            logger.log_event(t_id, "START BOT", f"Existing user {t_id}")

        if not user_info.get("language"):
            context.set_user_info_field(t_id, "language", t_language_code)
            context.save_user_info(t_id)
        else:
            t_language_code = user_info.get("language")

        _ensure_user_dir(user_info["id"])

        if user_info is None or _needs_initial_setup(user_info):
            lang_name = get_language_name(t_language_code)
            flag = get_language_flag(t_language_code)
            bot.set_state(t_id, SurveyStates.language_confirm, message.chat.id)
            bot.send_message(
                t_id,
                _safe_translation(t_id, "language_confirm").format(language=lang_name, flag=flag),
                parse_mode="HTML",
                reply_markup=consent_menu(t_id),
            )
            logger.log_event(t_id, "LANGUAGE_CONFIRM", t_language_code)
            return

        # Main menu path
        bot.set_state(t_id, SurveyStates.main_menu, message.chat.id)
        welcome = _safe_translation(t_id, "welcome_message")
        menu_msg = _safe_translation(t_id, "main_menu_message")
        bot.send_message(
            t_id,
            f"{welcome}\n\n{menu_msg}",
            parse_mode="HTML",
            reply_markup=main_menu(t_id),
        )
        logger.log_event(t_id, "MAIN_MENU", t_language_code)

    @bot.callback_query_handler(func=lambda call: call.data in ("yes", "no"), state=SurveyStates.language_confirm)
    def confirm_language(call: CallbackQuery):
        t_id = call.message.chat.id
        message_id = call.message.message_id
        if call.data == "yes":
            bot.set_state(t_id, SurveyStates.consent, call.message.chat.id)
            bot.edit_message_text(
                chat_id=t_id,
                message_id=message_id,
                text=_safe_translation(t_id, "consent_message"),
                parse_mode="HTML",
                reply_markup=consent_menu(t_id),
            )
            logger.log_event(t_id, "LANGUAGE_CONFIRMED", call.data)
        else:
            bot.set_state(t_id, SurveyStates.language, call.message.chat.id)
            bot.edit_message_text(
                chat_id=t_id,
                message_id=message_id,
                text=_safe_translation(t_id, "language_selection"),
                parse_mode="HTML",
                reply_markup=language_menu(),
            )
            logger.log_event(t_id, "LANGUAGE_RESELECT", call.data)