from __future__ import annotations
import os
from pathlib import Path
import telebot

from states import SurveyStates
from config import RESPONSES_DIR
from utils.storage import context, get_translation
from localization import (
    get_available_languages,
    get_language_name,
    get_language_flag,
    normalize_language,
)
from utils.menu import main_menu, consent_menu, language_menu
from utils.logger import logger
from flow.renderer import render_node, engine

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
            # Step 1: welcome (no menu), store its message id for later updates
            welcome_mid = render_node(
                bot,
                t_id,
                engine.start,  # 'welcome'
            )
            if welcome_mid is not None:
                context.set_user_info_field(t_id, "welcome_message_id", welcome_mid)
            # Step 2: language confirmation with yes/no
            render_node(
                bot,
                t_id,
                engine.next("welcome") or "language_confirm",
                fmt={"language": lang_name, "flag": flag},
                menu=consent_menu,
            )
            logger.log_event(t_id, "LANGUAGE_CONFIRM", t_language_code)
            return

        # Main menu path
        render_node(bot, t_id, "main_menu", menu=main_menu)
        logger.log_event(t_id, "MAIN_MENU", t_language_code)

    @bot.callback_query_handler(func=lambda call: call.data in ("yes", "no"), state=SurveyStates.language_confirm)
    def confirm_language(call: CallbackQuery):
        t_id = call.message.chat.id
        message_id = call.message.message_id
        if call.data == "yes":
            # proceed to consent directly
            render_node(
                bot,
                t_id,
                engine.next("language_confirm", event="yes") or "consent",
                message_id=message_id,
                menu=consent_menu,
            )
            logger.log_event(t_id, "LANGUAGE_CONFIRMED", call.data)
        else:
            # show language selection
            render_node(
                bot,
                t_id,
                engine.next("language_confirm", event="no") or "language",
                message_id=message_id,
                menu=lambda _tid: language_menu(),
            )
            logger.log_event(t_id, "LANGUAGE_RESELECT", call.data)