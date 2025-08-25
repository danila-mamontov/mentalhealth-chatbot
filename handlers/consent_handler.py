from __future__ import annotations
import telebot
from states import SurveyStates
from utils.logger import logger
from utils.storage import context
from flow.renderer import render_node, engine

def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data in ("yes", "no"), state=SurveyStates.consent)
    def handle_consent(call):
        t_id = call.message.chat.id
        message_id = call.message.message_id
        if call.data == "yes":
            context.set_user_info_field(t_id, "consent", "yes")
            context.save_user_info(t_id)
            logger.log_event(t_id, "SET CONSENT", "YES")
            next_node = engine.next("consent", event="yes") or "gender"
            render_node(bot, t_id, next_node, message_id=message_id)
        elif call.data == "no":
            context.set_user_info_field(t_id, "consent", "no")
            context.save_user_info(t_id)
            logger.log_event(t_id, "SET CONSENT", "NO")
            try:
                bot.delete_state(t_id)
            except Exception:
                pass
            next_node = engine.next("consent", event="no") or "help"
            render_node(bot, t_id, next_node, message_id=message_id)
