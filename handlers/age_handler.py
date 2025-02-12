import telebot
from telebot.types import CallbackQuery
from utils.menu import main_menu, exact_age_menu
from localization import get_translation
from config import RESPONSES_DIR
import os
import pandas as pd
from utils.storage import context

def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("range_"))
    def handle_age_range_selection(call):
        user_id = call.message.chat.id
        selected_range = call.data.split("_")[1]
        start_age, end_age = map(int, selected_range.split("-"))

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=get_translation(user_id, "age_selection"),
            reply_markup=exact_age_menu(user_id,start_age, end_age)
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("age_"))
    def handle_exact_age_selection(call):
        user_id = call.message.chat.id
        selected_age = call.data.split("_")[1]

        context.set_user_info_field(user_id, "age", int(selected_age))
        context.save_user_info(user_id)

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=get_translation(user_id, "main_menu_message"),
            parse_mode='HTML',
            reply_markup=main_menu(user_id)
        )