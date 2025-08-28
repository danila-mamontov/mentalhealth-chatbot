from __future__ import annotations
import telebot
from telebot.types import CallbackQuery

from states import SurveyStates
from utils.menu import consent_menu, language_menu
from utils.logger import logger
from flow.renderer import render_node, engine


def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data in ("yes", "no"), state=SurveyStates.language_confirm)
    def confirm_language(call: CallbackQuery):
        t_id = call.message.chat.id
        message_id = call.message.message_id

        if call.data == "yes":

            render_node(
                bot,
                t_id,
                engine.next("language_confirm", event="yes") or "consent",
                message_id=message_id,
                menu=consent_menu,
            )
            logger.log_event(t_id, "LANGUAGE_CONFIRMED", call.data)
        else:

            render_node(
                bot,
                t_id,
                engine.next("language_confirm", event="no") or "language_select",
                message_id=message_id,
                menu=lambda _tid: language_menu(),
            )
            logger.log_event(t_id, "LANGUAGE_RESELECT", call.data)