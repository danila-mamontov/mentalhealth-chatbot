import telebot
from utils.menu import yes_no_menu
from utils.storage import context, get_translation
from utils.db import save_session
from utils.logger import logger
from states import SurveyStates

def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(
        func=lambda call: call.data in ("yes", "no", "noanswer"),
        state=SurveyStates.treatment,
    )
    def handle_treatment_selection(call):
        user_id = call.message.chat.id
        treatment = call.data
        context.set_user_info_field(user_id,"treatment",treatment)
        context.save_user_info(user_id)
        logger.log_event(user_id, "SET TREATMENT",treatment)

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=get_translation(user_id, "depressive_feelings"),
            parse_mode="HTML",
            reply_markup=yes_no_menu(user_id),
        )
        bot.set_state(user_id, SurveyStates.depressive, call.message.chat.id)
        save_session(user_id, {"fsm_state": str(SurveyStates.depressive)})

