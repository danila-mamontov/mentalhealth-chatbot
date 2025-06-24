"""Handlers for the WBMMS voice survey using :mod:`survey_session`."""

from __future__ import annotations

import os
import telebot

from survey_session import SurveyManager, SurveySession
from utils.menu import survey_menu, main_menu
from survey import keycap_numbers, get_wbmms_question
from utils.storage import get_translation
from utils.logger import logger
from config import RESPONSES_DIR
from states import SurveyStates
from utils.db import insert_voice_metadata


def _save_voice_answers(bot: telebot.TeleBot, session: SurveySession) -> None:
    """Persist all recorded voice answers for ``session``."""

    user_id = session.user_id
    for _, meta in session.iter_voice_answers():
        filename = f"{user_id}_{meta.timestamp}_{meta.question_id}.ogg"
        file_path = os.path.join(RESPONSES_DIR, str(user_id), "audio", filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        data = bot.download_file(meta.file_path)
        with open(file_path, "wb") as f:
            f.write(data)
        insert_voice_metadata(
            user_id=user_id,
            question_id=meta.question_id,
            file_unique_id=meta.file_unique_id,
            file_path=file_path,
            duration=meta.duration,
            timestamp=meta.timestamp,
            file_size=len(data),
        )


def _render_question(bot: telebot.TeleBot, user_id: int, message_id: int, index: int) -> None:
    if index <= 9:
        keycap = keycap_numbers[index + 1]
    else:
        keycap = keycap_numbers[index // 10] + keycap_numbers[index % 10 + 1]
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=f"{keycap}\t" + get_wbmms_question(index, user_id=user_id),
        parse_mode="HTML",
        reply_markup=survey_menu(user_id, index),
    )


def register_handlers(bot: telebot.TeleBot) -> None:
    @bot.callback_query_handler(func=lambda c: c.data.startswith("survey_"), state=SurveyStates.wbmms)
    def handle_survey_buttons(call: telebot.types.CallbackQuery) -> None:
        user_id = call.message.chat.id
        session = SurveyManager.get_session(user_id)

        action = call.data
        if action == "survey_prev":
            _id = session.prev_question()
            logger.log_event(user_id, "WBMMS PREV", _id)
            _render_question(bot, user_id, call.message.message_id, session.current_index)
        elif action == "survey_next":
            _id = session.next_question()
            logger.log_event(user_id, "WBMMS NEXT", _id)
            _render_question(bot, user_id, call.message.message_id, session.current_index)
        elif action == "survey_delete":
            msg_id = session.delete_voice(session.current_index)
            if msg_id:
                try:
                    bot.delete_message(user_id, msg_id)
                except Exception:
                    pass
        elif action == "survey_finish":
            _save_voice_answers(bot, session)
            SurveyManager.remove_session(user_id)
            logger.log_event(user_id, "END WBMMS SURVEY")
            bot.edit_message_text(
                chat_id=user_id,
                message_id=call.message.message_id,
                text=get_translation(user_id, "end_phq9_message")
                + "\n\n"
                + get_translation(user_id, "main_menu_message"),
                parse_mode="HTML",
                reply_markup=main_menu(user_id),
            )
            bot.set_state(user_id, SurveyStates.main_menu, call.message.chat.id)

