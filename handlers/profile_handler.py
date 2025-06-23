import telebot
from utils.storage import get_user_profile
from utils.menu import profile_menu


def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("profile_"))
    def handle_profile_response(call):
        user_id = call.message.chat.id
        command = call.data.split("_")[1]
        if command == "open":
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=get_user_profile(user_id),
                parse_mode='HTML',
                reply_markup=profile_menu(user_id),
            )

