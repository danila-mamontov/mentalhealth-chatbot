import telebot
from telebot.types import CallbackQuery

from utils.storage import context
from utils.menu import consent_menu
from localization import get_translation
from utils.logger import logger


# Handler for language selection buttons
def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("set_language_"))
    def handle_language_selection(call):
        user_id = call.message.chat.id
        message_id = call.message.message_id
        language = call.data.split("_")[2]

        context.set_user_info_field(user_id, "language", language)
        context.save_user_info(user_id)
        logger.log_event(user_id, "SET LANGUAGE", language)

        bot.delete_message(user_id, message_id)
        bot.send_message(user_id, get_translation(user_id,"welcome_message"), parse_mode='HTML')
        bot.send_message(user_id, get_translation(user_id, "consent_message"), reply_markup=consent_menu(user_id))
