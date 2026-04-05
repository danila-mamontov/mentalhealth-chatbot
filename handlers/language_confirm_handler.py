from __future__ import annotations
import telebot
from telebot.types import CallbackQuery

from states import SurveyStates
from utils.menu import consent_menu, language_menu
from utils.logger import logger
from flow.renderer import render_node


def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data in ("yes", "no"), state=SurveyStates.language_confirm)
    def confirm_language(call: CallbackQuery):
        t_id = call.message.chat.id
        message_id = call.message.message_id

        # Always go to consent (language is already set to Russian in start_handler)
        render_node(
            bot,
            t_id,
            "consent",
            message_id=message_id,
            menu=consent_menu,
        )
        logger.log_event(t_id, "LANGUAGE_CONFIRMED_AUTO_RU", call.data)
