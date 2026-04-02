import telebot

from utils.storage import get_translation, context
from utils.logger import logger


def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("goto_"))
    def handle_goto_button(call):
        from utils.menu import main_menu, age_range_menu
        t_id = call.message.chat.id
        page = call.data

        logger.log_event(t_id, "BACK BUTTON", page)
        if page == "goto_age_range":
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=get_translation(t_id, "age_selection_msg"),
                                  parse_mode="HTML",
                                  reply_markup=age_range_menu(t_id))
        elif page == "goto_main_menu":
            menu_text = get_translation(t_id, "main_menu_msg")
            # Use database user_id instead of chat_id
            db_user_id = context._get_id(t_id)
            if db_user_id is not None:
                menu_text = menu_text.format(user_id=db_user_id)
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=menu_text,
                parse_mode="HTML",
                reply_markup=main_menu(t_id),
            )
        else:
            bot.answer_callback_query(call.id)
