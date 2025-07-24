import os
import shutil
import telebot
from utils.logger import logger
from utils.storage import context

def register_handlers(bot: telebot.TeleBot):
    @bot.message_handler(commands=['delete_me'])
    def delete_user_data(message):
        t_id = message.chat.id
        user_dir = os.path.join("responses", str(t_id))

        # remove user from in-memory context and database
        context.delete_user(t_id)

        # reset bot state and close any open log handlers
        bot.delete_state(t_id)
        logger.close(t_id)

        if os.path.exists(user_dir):
            try:
                shutil.rmtree(user_dir)
                bot.send_message(t_id, f"🗑 All your {t_id} data has been deleted successfully.")
            except Exception as e:
                bot.send_message(t_id, f"⚠️ Failed to delete data: {str(e)}")
        else:
            bot.send_message(t_id, "ℹ️ No data found to delete.")


