import telebot
from utils.storage import get_user_profile
from utils.menu import profile_menu
from states import EditProfileStates


def register_handlers(bot: telebot.TeleBot):
    """Register profile callbacks."""

    @bot.callback_query_handler(func=lambda call: call.data.startswith("profile_"))
    def handle_profile_response(call):
        t_id = call.message.chat.id
        command = call.data.split("_")[1]
        bot.set_state(t_id, EditProfileStates.editing_profile, call.message.chat.id)
        if command == "open":
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=get_user_profile(t_id),
                parse_mode="HTML",
                reply_markup=profile_menu(t_id),
            )
        else:
            bot.answer_callback_query(call.id)

