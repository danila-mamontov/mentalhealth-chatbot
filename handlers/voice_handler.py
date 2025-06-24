import telebot

from utils.storage import context, get_translation
from utils.logger import logger
from survey_session import SurveyManager, VoiceAnswer
from handlers import wbmms_survey_handler as wsh
from states import SurveyStates

def register_handlers(bot: telebot.TeleBot):
    @bot.message_handler(content_types=['voice'], state=SurveyStates.wbmms)
    def handle_voice_message(message):
        user_id = message.chat.id
        session = SurveyManager.get_session(user_id)
        current_question = session.current_index

        file_path = bot.get_file(message.voice.file_id).file_path
        audio_duration = message.voice.duration
        file_unique_id = message.voice.file_unique_id
        file_id = message.voice.file_id

        va = VoiceAnswer(
            user_id=user_id,
            question_id=current_question,
            file_unique_id=file_unique_id,
            file_id=file_id,
            file_path=file_path,
            duration=audio_duration,
            timestamp=message.date,
            file_size=0,
        )
        session.record_voice(message.message_id, va)

        # persist immediately and clean up original message
        wsh._save_voice_answers(bot, session, current_question)

        # re-send the voice message from bot account
        try:
            sent = bot.send_voice(user_id, file_id)
        except Exception:
            sent = None
        else:
            # replace stored message id with the bot-sent one
            session.voice_messages.pop(message.message_id, None)
            session.voice_messages[sent.message_id] = va
            ids = session.question_voice_ids.get(current_question, [])
            try:
                idx = ids.index(message.message_id)
                ids[idx] = sent.message_id
            except ValueError:
                ids.append(sent.message_id)

        logger.log_event(user_id, f"VOICE WBMMS QUESTION {current_question}", f"answer id {file_unique_id}")

        prefix = get_translation(user_id, "voice_recieved")
        wsh._update_controls(bot, session, prefix)

        # if audio_duration < 5:
        #     bot.send_message(message.chat.id, "⚠️ Голосовое сообщение слишком короткое!")
        # else:
        #     timestamp = message.date
        #     current_question = context.get_user_info_field(user_id, "current_question_index")
        #
        #     filename = f"{user_id}_{timestamp}_{current_question}.ogg"
        #     file_path = os.path.join(RESPONSES_DIR, f"{user_id}", "audio", filename)
        #     with open(file_path, 'wb') as f:
        #         downloaded_file = bot.download_file(file_info.file_path)
        #         f.write(downloaded_file)
        #     pd.DataFrame({'user_id': [user_id],'timestamp': [timestamp], 'duration': [audio_duration]}).to_csv("stats.csv", mode='a', header=False, index=False)
        #
        #
        #     context.set_user_info_field(user_id, "current_question_index", current_question + 1)
        #     logger.log_event(user_id, f"VOICE WBMMS QUESTION {current_question}", f"answer {filename}")
        #     ask_next_main_question(bot, user_id)

