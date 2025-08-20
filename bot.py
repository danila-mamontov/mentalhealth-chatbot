import os
import telebot
from telebot import custom_filters
from telebot.storage import StateMemoryStorage

from config import BOT_TOKEN, RESPONSES_DIR, API_URL, LOCAL_SERVER_MODE
from handlers import (
    goto_handler,
    start_handler,
    help_handler,
    delete_me_handler,
    consent_handler,
    gender_handler,
    age_handler,
    main_menu_handler,
    profile_handler,
    phq9_survey_handler,
    wbmms_survey_handler,
    voice_handler,
    language_handler,
    treatment_handler,
    depressive_handler,
)

if LOCAL_SERVER_MODE:
    print("Running in local server mode")
    try:
        bot = telebot.TeleBot(BOT_TOKEN, state_storage=StateMemoryStorage())
        bot.log_out()
        print("Bot logged out successfully")
    except Exception as e:
        print(f"{e}")
    telebot.apihelper.API_URL = API_URL

bot = telebot.TeleBot(BOT_TOKEN, state_storage=StateMemoryStorage())
bot.add_custom_filter(custom_filters.StateFilter(bot))

# Регистрация обработчиков

start_handler.register_handlers(bot)
delete_me_handler.register_handlers(bot)
language_handler.register_handlers(bot)
consent_handler.register_handlers(bot)
age_handler.register_handlers(bot)
gender_handler.register_handlers(bot)
profile_handler.register_handlers(bot)
goto_handler.register_handlers(bot)

main_menu_handler.register_handlers(bot)
phq9_survey_handler.register_handlers(bot)
wbmms_survey_handler.register_handlers(bot)
treatment_handler.register_handlers(bot)
depressive_handler.register_handlers(bot)
voice_handler.register_handlers(bot)
help_handler.register_handlers(bot)

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
