import telebot
from utils.storage import get_translation
from utils.user_map import get_user_id


def register_handlers(bot: telebot.TeleBot):
    @bot.message_handler(commands=["help"])
    def handle_help(message):
        telegram_id = message.chat.id
        user_id = get_user_id(telegram_id)
        bot.send_message(telegram_id, get_translation(user_id, "help"), parse_mode="HTML")
