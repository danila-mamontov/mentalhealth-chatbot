"""Handler for the reading text stage - users record themselves reading a passage."""

import telebot
from utils.storage import context, get_translation
from utils.logger import logger
from survey_session import SurveyManager, VoiceAnswer
from states import SurveyStates
from config import RESPONSES_DIR, LOCAL_SERVER_MODE
from utils.db import insert_voice_metadata
import os
import shutil


def register_handlers(bot: telebot.TeleBot):
    """Register handlers for the reading text stage."""

    @bot.message_handler(state=SurveyStates.reading_text, content_types=['voice'])
    def handle_reading_text_voice(message):
        """
        Handle voice message with the read text.
        Save the voice file and transition to final menu.
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

        # Delete original message
        try:
            bot.delete_message(t_id, message.message_id)
        except Exception:
            pass

        # Log the event
        logger.log_event(
            t_id, "VOICE READING TEXT", f"answer id {file_unique_id}"
        )

        # Set state to final menu
        bot.set_state(t_id, SurveyStates.final_menu, t_id)

        # Show final menu by editing existing message
        user_id = context.get_user_info_field(t_id, "id")
        menu_msg = get_translation(t_id, "final_menu_msg").format(user_id=user_id)

        from utils.menu import final_menu

        # Get the reading text message ID to edit it
        reading_text_msg_id = context.get_user_info_field(t_id, "message_to_del")
        if reading_text_msg_id:
            try:
                bot.edit_message_text(
                    chat_id=t_id,
                    message_id=reading_text_msg_id,
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
        else:
            # If no message ID stored, send a new message
            bot.send_message(
                t_id,
                menu_msg,
                parse_mode="HTML",
                reply_markup=final_menu(t_id),
            )

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







