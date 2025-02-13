import os
import telebot
from telebot.types import BotCommand
import pandas as pd
from win32comext.adsi.demos.scp import logger

from config import BOT_TOKEN, RESPONSES_DIR
from handlers import start_handler, help_handler, consent_handler,gender_handler ,age_handler,main_menu_handler, phq9_survey_handler,wbmms_survey_handler,voice_handler, language_handler
bot = telebot.TeleBot(BOT_TOKEN)

# Регистрация обработчиков

start_handler.register_handlers(bot)
language_handler.register_handlers(bot)
consent_handler.register_handlers(bot)
age_handler.register_handlers(bot)
gender_handler.register_handlers(bot)

main_menu_handler.register_handlers(bot)
phq9_survey_handler.register_handlers(bot)
wbmms_survey_handler.register_handlers(bot)
voice_handler.register_handlers(bot)
help_handler.register_handlers(bot)


bot.set_my_commands([
    BotCommand("start", "Start the bot"),
    BotCommand("help", "All available commands"),
    BotCommand("language", "Select language"),
    BotCommand("support", "Contact the support team"),
    BotCommand("stop", "Stop the bot")
])

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
