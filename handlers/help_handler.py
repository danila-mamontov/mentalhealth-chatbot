import telebot
from utils.storage import get_translation


def register_handlers(bot: telebot.TeleBot) -> None:
    @bot.message_handler(commands=["help"])
    def handle_help(message: telebot.types.Message) -> None:
        user_id = message.chat.id
        bot.send_message(user_id, get_translation(user_id, "help"), parse_mode="HTML")
