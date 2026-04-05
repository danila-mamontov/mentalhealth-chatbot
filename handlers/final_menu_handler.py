"""Handlers for the final menu stage."""

import telebot
from utils.menu import main_menu
from utils.storage import context, get_translation
from utils.logger import logger
from states import SurveyStates


def register_handlers(bot: telebot.TeleBot):
    """Register handlers for the final menu stage."""

    @bot.callback_query_handler(
        func=lambda call: call.data == "switch_inline_query",
        state=SurveyStates.final_menu,
    )
    def handle_final_menu_share(call):
        """Handle share button in final menu."""
        t_id = call.message.chat.id
        logger.log_event(t_id, "FINAL MENU SHARE", "triggered")

        # Show main menu
        user_id = context.get_user_info_field(t_id, "id")
        menu_msg = get_translation(t_id, "main_menu_msg").format(user_id=user_id)

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=menu_msg,
            parse_mode="HTML",
            reply_markup=main_menu(t_id),
        )
        bot.set_state(t_id, SurveyStates.main_menu, call.message.chat.id)

    @bot.message_handler(state=SurveyStates.final_menu, commands=['start', 'help'])
    def handle_final_menu_commands(message: telebot.types.Message) -> None:
        """Handle /start and /help commands in final menu."""
        t_id = message.chat.id
        user_id = context.get_user_info_field(t_id, "id")
        menu_msg = get_translation(t_id, "main_menu_msg").format(user_id=user_id)

        bot.send_message(
            t_id,
            menu_msg,
            parse_mode="HTML",
            reply_markup=main_menu(t_id),
        )
        bot.set_state(t_id, SurveyStates.main_menu, t_id)

