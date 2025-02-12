import telebot
from telebot.types import CallbackQuery
from utils.menu import age_range_menu
from localization import get_translation
from config import RESPONSES_DIR
import os
import pandas as pd
from utils.storage import context

def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("set_gender_"))
    def handle_gender_selection(call: CallbackQuery):
        user_id = call.message.chat.id
        gender = call.data.split("_")[-1]
        context.set_user_info_field(user_id,"gender",gender)
        context.save_user_info(user_id)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=get_translation(user_id, "age_selection"),
                              parse_mode="HTML",
                              reply_markup=age_range_menu(user_id))



