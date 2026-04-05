"""Handler for the reading text stage - users record themselves reading a passage."""

import telebot
from utils.storage import context, get_translation
from utils.logger import logger
from survey_session import VoiceAnswer
from states import SurveyStates
from config import RESPONSES_DIR, LOCAL_SERVER_MODE
from utils.db import insert_voice_metadata
from utils.menu import confirm_menu
import os
import shutil


def register_handlers(bot: telebot.TeleBot):
    """Register handlers for the reading text stage."""

    @bot.message_handler(state=SurveyStates.reading_text, content_types=['voice'])
    def handle_reading_text_voice(message):
        """
        Handle voice message with the read text.
        Save the voice file, delete user's message, and resend from bot.
        """
        t_id = message.chat.id

        # Get file info
        file_path = bot.get_file(message.voice.file_id).file_path
        audio_duration = message.voice.duration
        file_unique_id = message.voice.file_unique_id
        file_id = message.voice.file_id

        # Create voice answer metadata
        va = VoiceAnswer(
            t_id=t_id,
            question_id=-1,  # Special ID for reading text task
            file_unique_id=file_unique_id,
            file_id=file_id,
            file_path=file_path,
            duration=audio_duration,
            timestamp=message.date,
            file_size=0,
        )

        # Get user ID and prepare file path
        uid = context.get_user_info_field(t_id, "id")
        if uid is None:
            context.add_new_user(t_id)
            uid = context.get_user_info_field(t_id, "id")

        filename = f"{message.date}_reading_text.ogg"
        local_path = os.path.join(RESPONSES_DIR, str(uid), "audio", filename)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        # Save the voice file
        if LOCAL_SERVER_MODE:
            shutil.copy(file_path, local_path)
            data = open(local_path, "rb").read()
        else:
            data = bot.download_file(file_path)
            with open(local_path, "wb") as f:
                f.write(data)

        # Insert metadata to database
        insert_voice_metadata(
            user_id=uid,
            question_id=-1,
            file_unique_id=file_unique_id,
            file_path=local_path,
            duration=audio_duration,
            timestamp=message.date,
            file_size=len(data),
        )
        va.saved = True
        va.file_size = len(data)
        va.file_path = local_path

        # Delete user's voice message
        try:
            bot.delete_message(t_id, message.message_id)
        except Exception:
            pass

        # Log the event
        logger.log_event(
            t_id, "VOICE READING TEXT", f"answer id {file_unique_id}"
        )

        # Accumulate duration for all recordings
        current_duration = context.get_user_info_field(t_id, "reading_text_total_duration") or 0
        total_duration = current_duration + audio_duration
        context.set_user_info_field(t_id, "reading_text_total_duration", total_duration)

        # Resend voice from bot account and track the message
        try:
            sent_voice = bot.send_voice(t_id, file_id)
            # Update voice message ID tracking
            prev_voice_msg_id = context.get_user_info_field(t_id, "reading_text_voice_msg_id")
            if prev_voice_msg_id:
                try:
                    bot.delete_message(t_id, prev_voice_msg_id)
                except Exception:
                    pass
            context.set_user_info_field(t_id, "reading_text_voice_msg_id", sent_voice.message_id)
        except Exception:
            pass

    @bot.message_handler(state=SurveyStates.reading_text_confirm, content_types=['voice'])
    def handle_reading_text_voice_in_confirm(message):
        """Handle voice messages while in confirmation state - resend them."""
        t_id = message.chat.id

        # Get file info
        file_path = bot.get_file(message.voice.file_id).file_path
        audio_duration = message.voice.duration
        file_unique_id = message.voice.file_unique_id
        file_id = message.voice.file_id

        # Create voice answer metadata
        va = VoiceAnswer(
            t_id=t_id,
            question_id=-1,
            file_unique_id=file_unique_id,
            file_id=file_id,
            file_path=file_path,
            duration=audio_duration,
            timestamp=message.date,
            file_size=0,
        )

        # Get user ID and prepare file path
        uid = context.get_user_info_field(t_id, "id")
        if uid is None:
            return

        filename = f"{message.date}_reading_text.ogg"
        local_path = os.path.join(RESPONSES_DIR, str(uid), "audio", filename)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        # Save the voice file
        if LOCAL_SERVER_MODE:
            shutil.copy(file_path, local_path)
            data = open(local_path, "rb").read()
        else:
            data = bot.download_file(file_path)
            with open(local_path, "wb") as f:
                f.write(data)

        # Insert metadata to database
        insert_voice_metadata(
            user_id=uid,
            question_id=-1,
            file_unique_id=file_unique_id,
            file_path=local_path,
            duration=audio_duration,
            timestamp=message.date,
            file_size=len(data),
        )
        va.saved = True
        va.file_size = len(data)
        va.file_path = local_path

        # Delete user's voice message
        try:
            bot.delete_message(t_id, message.message_id)
        except Exception:
            pass

        # Log the event
        logger.log_event(
            t_id, "VOICE READING TEXT CONFIRM", f"answer id {file_unique_id}"
        )

        # Accumulate duration
        current_duration = context.get_user_info_field(t_id, "reading_text_total_duration") or 0
        total_duration = current_duration + audio_duration
        context.set_user_info_field(t_id, "reading_text_total_duration", total_duration)

        # Resend voice from bot account and track the message
        try:
            sent_voice = bot.send_voice(t_id, file_id)
            # Update voice message ID tracking
            prev_voice_msg_id = context.get_user_info_field(t_id, "reading_text_voice_msg_id")
            if prev_voice_msg_id:
                try:
                    bot.delete_message(t_id, prev_voice_msg_id)
                except Exception:
                    pass
            context.set_user_info_field(t_id, "reading_text_voice_msg_id", sent_voice.message_id)
        except Exception:
            pass

    @bot.callback_query_handler(
        func=lambda call: call.data == "yes",
        state=SurveyStates.reading_text_confirm,
    )
    def handle_reading_text_confirmation(call):
        """Handle user confirmation of reading text completion."""
        t_id = call.message.chat.id
        message_id = call.message.message_id

        # Check voice duration on confirmation
        MIN_DURATION = 10
        total_duration = context.get_user_info_field(t_id, "reading_text_total_duration") or 0
        if total_duration < MIN_DURATION:
            try:
                bot.answer_callback_query(
                    call.id,
                    text=get_translation(t_id, "reading_text_too_short_msg"),
                    show_alert=True,
                )
            except Exception:
                pass
            return

        # User confirmed - proceed to final menu
        logger.log_event(t_id, "READING TEXT CONFIRMED", "yes")

        # Delete the voice message that was sent for verification
        voice_msg_id = context.get_user_info_field(t_id, "reading_text_voice_msg_id")
        if voice_msg_id:
            try:
                bot.delete_message(t_id, voice_msg_id)
            except Exception:
                pass
            context.set_user_info_field(t_id, "reading_text_voice_msg_id", None)

        # Delete the reading text instruction message
        reading_text_msg_id = context.get_user_info_field(t_id, "message_to_del")
        if reading_text_msg_id:
            try:
                bot.delete_message(t_id, reading_text_msg_id)
            except Exception:
                pass
            context.set_user_info_field(t_id, "message_to_del", None)

        # Clear accumulated duration
        context.set_user_info_field(t_id, "reading_text_total_duration", None)

        # Show final menu by editing confirmation message
        user_id = context.get_user_info_field(t_id, "id")
        end_survey_msg = get_translation(t_id, "end_main_survey_msg").format(user_id=user_id)
        final_menu_msg = get_translation(t_id, "final_menu_msg").format(user_id=user_id)
        menu_msg = end_survey_msg + "\n\n" + final_menu_msg

        from utils.menu import final_menu

        try:
            bot.edit_message_text(
                chat_id=t_id,
                message_id=message_id,
                text=menu_msg,
                parse_mode="HTML",
                reply_markup=final_menu(t_id),
            )
        except Exception:
            # If edit fails, send a new message
            bot.send_message(
                t_id,
                menu_msg,
                parse_mode="HTML",
                reply_markup=final_menu(t_id),
            )

        bot.set_state(t_id, SurveyStates.final_menu, t_id)

    @bot.message_handler(state=SurveyStates.reading_text, commands=['start', 'help'])
    def handle_reading_text_commands(message: telebot.types.Message) -> None:
        """Handle /start and /help commands in reading text state."""
        t_id = message.chat.id
        instruction_msg = get_translation(t_id, "reading_text_instruction_msg")
        text_to_read = get_translation(t_id, "reading_text_content_msg")

        bot.send_message(
            t_id,
            instruction_msg + "\n\n" + text_to_read,
            parse_mode="HTML",
        )





































