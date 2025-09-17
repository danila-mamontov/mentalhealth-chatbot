import telebot

from utils.storage import context, get_translation
from utils.logger import logger
from survey_session import SurveyManager, VoiceAnswer
import handlers.main_survey_handler as msh
from states import SurveyStates
from config import RESPONSES_DIR, LOCAL_SERVER_MODE
from utils.db import insert_voice_metadata
import os
import shutil

def register_handlers(bot: telebot.TeleBot):
    @bot.message_handler(content_types=['voice'], state=SurveyStates.main)
    def handle_voice_message(message):
        t_id = message.chat.id
        session = SurveyManager.get_session(t_id)
        current_question = session.current_index

        file_path = bot.get_file(message.voice.file_id).file_path
        audio_duration = message.voice.duration
        file_unique_id = message.voice.file_unique_id
        file_id = message.voice.file_id

        va = VoiceAnswer(
            t_id=t_id,
            question_id=current_question,
            file_unique_id=file_unique_id,
            file_id=file_id,
            file_path=file_path,
            duration=audio_duration,
            timestamp=message.date,
            file_size=0,
        )
        session.record_voice(message.message_id, va)

        # persist the new voice and remove the original message
        filename = f"{message.date}_{current_question}.ogg"
        uid = context.get_user_info_field(t_id, "id")
        if uid is None:
            context.add_new_user(t_id)
            uid = context.get_user_info_field(t_id, "id")
        local_path = os.path.join(RESPONSES_DIR, str(uid), "audio", filename)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        if LOCAL_SERVER_MODE:
            # In local server mode, we can directly save the file from the bot's file system
            shutil.copy(file_path, local_path,)
            data = open(local_path, "rb").read()
        else:
            # In remote server mode, we need to use the file_path to download from the telegram server
            data = bot.download_file(file_path)
            with open(local_path, "wb") as f:
                f.write(data)
        insert_voice_metadata(
            user_id=uid,
            question_id=current_question,
            file_unique_id=file_unique_id,
            file_path=local_path,
            duration=audio_duration,
            timestamp=message.date,
            file_size=len(data),
        )
        va.saved = True
        va.file_size = len(data)
        va.file_path = local_path

        try:
            bot.delete_message(t_id, message.message_id)
        except Exception:
            pass

        # resend only the newly saved voice from the bot account
        try:
            sent = bot.send_voice(t_id, file_id)
        except Exception:
            sent = None
        else:
            session.voice_messages.pop(message.message_id, None)
            session.voice_messages[sent.message_id] = va
            ids = session.question_voice_ids.get(current_question, [])
            try:
                idx = ids.index(message.message_id)
                ids[idx] = sent.message_id
            except ValueError:
                ids.append(sent.message_id)

        prefix = get_translation(t_id, "voice_recieved_msg")
        msh._update_controls(bot, session, prefix, relocate=True)

        logger.log_event(
            t_id, f"VOICE MAIN QUESTION {current_question}", f"answer id {file_unique_id}"
        )

        # if audio_duration < 5:
        #     bot.send_message(message.chat.id, "⚠️ Голосовое сообщение слишком короткое!")
        # else:
        #     timestamp = message.date
        #     current_question = context.get_user_info_field(t_id, "current_question_index")
        #
        #     filename = f"{t_id}_{timestamp}_{current_question}.ogg"
        #     file_path = os.path.join(RESPONSES_DIR, f"{t_id}", "audio", filename)
        #     with open(file_path, 'wb') as f:
        #         downloaded_file = bot.download_file(file_info.file_path)
        #         f.write(downloaded_file)
        #     pd.DataFrame({'t_id': [t_id],'timestamp': [timestamp], 'duration': [audio_duration]}).to_csv("stats.csv", mode='a', header=False, index=False)
        #
        #
        #     context.set_user_info_field(t_id, "current_question_index", current_question + 1)
        #     logger.log_event(t_id, f"VOICE WBMMS QUESTION {current_question}", f"answer {filename}")
        #     ask_next_main_question(bot, t_id)
