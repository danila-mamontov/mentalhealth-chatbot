from __future__ import annotations
from utils.storage import get_translation


def register_handlers(bot):
    @bot.message_handler(commands=["help"])
    def handle_help(message):
        t_id = message.chat.id
        bot.send_message(t_id, get_translation(t_id, "help_msg"), parse_mode="HTML")
