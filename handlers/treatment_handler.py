import telebot
from utils.menu import yes_no_menu, main_menu, final_menu
from utils.storage import context, get_translation
from utils.logger import logger
from states import SurveyStates

def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(
        func=lambda call: call.data in ("yes", "no", "noanswer"),
        state=SurveyStates.treatment,
    )
    def handle_treatment_selection(call):
        t_id = call.message.chat.id
        treatment = call.data
        context.set_user_info_field(t_id,"treatment",treatment)
        context.save_user_info(t_id)
        logger.log_event(t_id, "SET TREATMENT",treatment)

        # Format end_main_survey_msg with user_id from database
        end_survey_text = get_translation(t_id, "end_main_survey_msg")
        db_user_id = context._get_id(t_id)
        if db_user_id is not None:
            end_survey_text = end_survey_text.format(user_id=db_user_id)

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=end_survey_text
            + "\n\n"
            + get_translation(t_id, "final_menu_msg"),
            parse_mode="HTML",
            reply_markup=final_menu(t_id),
        )
        bot.set_state(t_id, SurveyStates.final_menu, call.message.chat.id)
