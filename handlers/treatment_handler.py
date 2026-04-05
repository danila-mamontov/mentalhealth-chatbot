import telebot
from utils.menu import yes_no_menu, main_menu, final_menu, confirm_menu
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

        # Move to reading text stage with confirmation shown immediately
        reading_text_intro = get_translation(t_id, "reading_text_intro_msg")
        reading_text_content = get_translation(t_id, "reading_text_content_msg")
        reading_text_instruction = get_translation(t_id, "reading_text_instruction_msg")
        confirmation_msg = get_translation(t_id, "reading_text_confirm_msg")

        # Show reading text with confirmation button
        full_msg = reading_text_intro + "\n\n" + reading_text_content + "\n\n" + reading_text_instruction + "\n\n" + confirmation_msg

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=full_msg,
            parse_mode="HTML",
            reply_markup=confirm_menu(t_id),
        )
        # Store message ID for later editing to final menu
        context.set_user_info_field(t_id, "message_to_del", call.message.message_id)
        context.set_user_info_field(t_id, "reading_text_confirm_msg_id", call.message.message_id)

        # Initialize reading text total duration
        context.set_user_info_field(t_id, "reading_text_total_duration", 0)

        # Transition directly to reading_text_confirm state for voice messages
        bot.set_state(t_id, SurveyStates.reading_text_confirm, call.message.chat.id)
        logger.log_event(t_id, "READING TEXT STAGE", "started")

