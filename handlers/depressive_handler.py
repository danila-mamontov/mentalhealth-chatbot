import telebot
from utils.menu import main_menu
from utils.storage import context, get_translation
from utils.user_map import get_user_id
from utils.logger import logger
from states import SurveyStates

def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(
        func=lambda call: call.data in ("yes", "no", "noanswer"),
        state=SurveyStates.depressive,
    )
    def handle_depressive_selection(call):
        telegram_id = call.message.chat.id
        user_id = get_user_id(telegram_id)
        depressive = call.data
        context.set_user_info_field(user_id,"depressive",depressive)
        context.save_user_info(user_id)
        logger.log_event(user_id, "SET DEPRESSIVE",depressive)

        bot.edit_message_text(
            chat_id=telegram_id,
            message_id=call.message.message_id,
            text=get_translation(user_id, "end_main_survey_message")
            + "\n\n"
            + get_translation(user_id, "main_menu_message"),
            parse_mode="HTML",
            reply_markup=main_menu(user_id),
        )
        bot.set_state(user_id, SurveyStates.main_menu, call.message.chat.id)

