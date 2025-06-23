import telebot
from telebot.types import CallbackQuery
from utils.menu import main_menu
from utils.storage import context, get_translation
from utils.logger import logger

def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data in ("yes", "no", "noanswer"))
    def handle_depression_selection(call: CallbackQuery):
        user_id = call.message.chat.id
        depressive = call.data
        context.set_user_info_field(user_id,"depression",depressive)
        context.save_user_info(user_id)
        logger.log_event(user_id, "SET DEPRESSION",depressive)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=get_translation(user_id, "depression_selection"),
                              parse_mode="HTML",
                              reply_markup=main_menu(user_id))

