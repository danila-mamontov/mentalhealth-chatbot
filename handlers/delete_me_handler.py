import os
import shutil
import telebot
from utils.logger import logger
from utils.storage import context
from utils.user_map import get_user_id

def register_handlers(bot: telebot.TeleBot):
    @bot.message_handler(commands=['delete_me'])
    def delete_user_data(message):
        telegram_id = message.chat.id
        user_id = get_user_id(telegram_id)
        user_dir = os.path.join("responses", str(user_id))

        # remove user from in-memory context and database
        context.delete_user(user_id)

        # reset bot state and close any open log handlers
        bot.delete_state(user_id)
        logger.close(user_id)

        if os.path.exists(user_dir):
            try:
                shutil.rmtree(user_dir)
                bot.send_message(telegram_id, f"🗑 All your {user_id} data has been deleted successfully.")
            except Exception as e:
                bot.send_message(telegram_id, f"⚠️ Failed to delete data: {str(e)}")
        else:
            bot.send_message(telegram_id, "ℹ️ No data found to delete.")


