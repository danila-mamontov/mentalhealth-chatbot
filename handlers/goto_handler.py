import telebot
from telebot.types import CallbackQuery

from utils.storage import get_translation
from utils.logger import logger


def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("goto_"))
    def handle_goto_button(call: CallbackQuery):
        from utils.menu import main_menu, age_range_menu
        user_id = call.message.chat.id
        page = call.data

        logger.log_event(user_id, "BACK BUTTON", page)
        if page == "goto_age_range":
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=get_translation(user_id, "age_selection"),
                parse_mode="HTML",
                reply_markup=age_range_menu(user_id),
            )
        elif page == "goto_main_menu":
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=get_translation(user_id, "welcome_message") + "\n\n" + get_translation(user_id, "main_menu_message"),
                parse_mode="HTML",
                reply_markup=main_menu(user_id),
            )

