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

        # Move to reading text stage
        reading_text_intro = get_translation(t_id, "reading_text_intro_msg")
        reading_text_content = get_translation(t_id, "reading_text_content_msg")
        reading_text_instruction = get_translation(t_id, "reading_text_instruction_msg")

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=reading_text_intro + "\n\n" + reading_text_content + "\n\n" + reading_text_instruction,
            parse_mode="HTML",
        )
        # Store message ID for later editing to final menu
        context.set_user_info_field(t_id, "message_to_del", call.message.message_id)
        bot.set_state(t_id, SurveyStates.reading_text, call.message.chat.id)
        logger.log_event(t_id, "READING TEXT STAGE", "started")

