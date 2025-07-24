import telebot
from utils.menu import main_menu
from utils.storage import context, get_translation
from utils.logger import logger
from states import SurveyStates

def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(
        func=lambda call: call.data in ("yes", "no", "noanswer"),
        state=SurveyStates.depressive,
    )
    def handle_depressive_selection(call):
        t_id = call.message.chat.id
        depressive = call.data
        context.set_user_info_field(t_id,"depressive",depressive)
        context.save_user_info(t_id)
        logger.log_event(t_id, "SET DEPRESSIVE",depressive)

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=get_translation(t_id, "end_main_survey_message")
            + "\n\n"
            + get_translation(t_id, "main_menu_message"),
            parse_mode="HTML",
            reply_markup=main_menu(t_id),
        )
        bot.set_state(t_id, SurveyStates.main_menu, call.message.chat.id)

