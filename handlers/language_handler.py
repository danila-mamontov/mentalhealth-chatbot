import telebot
from telebot.types import CallbackQuery

from utils.storage import context, get_user_profile, get_translation
from utils.menu import consent_menu, language_menu, profile_menu
from utils.logger import logger


# Handler for language selection buttons
def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("set_language_"))
    def handle_language_selection(call):
        user_id = call.message.chat.id
        message_id = call.message.message_id
        language = call.data.split("_")[2]

        if language != "change":
            context.set_user_info_field(user_id, "language", language)
            context.save_user_info(user_id)
            logger.log_event(user_id, "SET LANGUAGE", language)
            if not context.get_user_info_field(user_id, "consent"):
                bot.send_message(user_id, get_translation(user_id, "consent_message"), reply_markup=consent_menu(user_id))
            else:
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=get_user_profile(user_id),
                    parse_mode='HTML',
                    reply_markup=profile_menu(user_id),
                )
        else:
            logger.log_event(user_id, "CHANGE LANGUAGE", "")
            bot.edit_message_text(chat_id=user_id,
                                  message_id=message_id,
                                  text=get_translation(user_id, "language_selection"),
                                  parse_mode='HTML',
                                  reply_markup=language_menu())
