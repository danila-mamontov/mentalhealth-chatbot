"""Handlers for the WBMMS voice survey using :mod:`survey_session`."""

from __future__ import annotations

import os
import telebot


from survey_session import SurveyManager, SurveySession, VoiceAnswer
from utils.menu import survey_menu, main_menu
from survey import keycap_numbers, get_wbmms_question
from utils.storage import context, get_translation
from utils.logger import logger
from config import RESPONSES_DIR
from states import SurveyStates
from utils.db import insert_voice_metadata


def get_controls_placeholder(user_id: int) -> str:
    """Return default controls message prompting for a voice reply."""
    return get_translation(user_id, "voice_answer_expected")


def _save_voice_answers(
    bot: telebot.TeleBot,
    session: SurveySession,
    question_index: int | None = None,
) -> None:
    """Persist any unsaved voice answers.

    If ``question_index`` is provided, only answers for that question are
    persisted. Previously saved answers are skipped.
    """

    user_id = session.user_id
    for msg_id, meta in list(session.iter_voice_answers()):
        if question_index is not None and meta.question_id != question_index:
            continue

        try:
            bot.delete_message(user_id, msg_id)
        except Exception:
            pass

        if not meta.saved:
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
            meta.saved = True
            meta.file_size = len(data)
            meta.file_path = file_path




def _render_question(
    bot: telebot.TeleBot,
    session: SurveySession,
    message_id: int,
    prefix: str | None = None,
) -> None:
    """Update survey prompt and show any recorded voices."""

    user_id = session.user_id
    index = session.current_index
    if index <= 9:
        keycap = keycap_numbers[index + 1]
    else:
        keycap = keycap_numbers[index // 10] + keycap_numbers[index % 10 + 1]
    text = f"{keycap}\t" + get_wbmms_question(index, user_id=user_id)

    try:
        bot.edit_message_text(
            chat_id=user_id,
            message_id=message_id,
            text=text,
            parse_mode="HTML",
        )
    except Exception as e:  # Telegram may raise if text is unchanged
        if "not modified" not in str(e).lower():
            raise

    voice_ids = session.question_voice_ids.get(index, [])
    new_ids: list[int] = []

    if voice_ids:
        controls_id = context.get_user_info_field(user_id, "survey_controls_id")
        if controls_id:
            try:
                bot.delete_message(user_id, controls_id)
            except Exception:
                pass
            context.set_user_info_field(user_id, "survey_controls_id", None)

        for vid in voice_ids:
            meta = session.voice_messages.get(vid)
            if not meta:
                continue
            sent = bot.send_voice(user_id, meta.file_id)
            session.voice_messages.pop(vid, None)
            session.voice_messages[sent.message_id] = meta
            new_ids.append(sent.message_id)

        if new_ids:
            session.question_voice_ids[index] = new_ids

        _update_controls(bot, session, prefix, relocate=True)
    else:
        _update_controls(bot, session, prefix, relocate=False)


def _update_controls(
    bot: telebot.TeleBot,
    session: SurveySession,
    prefix: str | None = None,
    relocate: bool = True,
) -> None:
    """Show or refresh the control buttons at the bottom of the chat."""

    user_id = session.user_id
    controls_id = context.get_user_info_field(user_id, "survey_controls_id")
    text = prefix if prefix is not None else get_controls_placeholder(user_id)
    markup = survey_menu(
        user_id, session.current_index, len(session.question_voice_ids.get(session.current_index, []))
    )

    if relocate:
        if controls_id:
            try:
                bot.delete_message(user_id, controls_id)
            except Exception:
                pass
            controls_id = None

    if controls_id and not relocate:
        try:
            bot.edit_message_text(
                chat_id=user_id,
                message_id=controls_id,
                text=text,
                parse_mode="HTML",
                reply_markup=markup,
            )
            return
        except Exception as e:
            if "not modified" in str(e).lower():
                return

    sent = bot.send_message(
        chat_id=user_id,
        text=text,
        parse_mode="HTML",
        reply_markup=markup,
    )
    context.set_user_info_field(user_id, "survey_controls_id", sent.message_id)


def register_handlers(bot: telebot.TeleBot) -> None:
    @bot.callback_query_handler(func=lambda c: c.data.startswith("survey_"), state=SurveyStates.wbmms)
    def handle_survey_buttons(call: telebot.types.CallbackQuery) -> None:
        user_id = call.message.chat.id
        session = SurveyManager.get_session(user_id)

        action = call.data
        question_id = context.get_user_info_field(user_id, "survey_message_id")
        if action == "survey_prev":
            _save_voice_answers(bot, session, session.current_index)
            _id = session.prev_question()
            logger.log_event(user_id, "WBMMS PREV", _id)
            _render_question(bot, session, question_id)
        elif action == "survey_next":
            _save_voice_answers(bot, session, session.current_index)
            _id = session.next_question()
            logger.log_event(user_id, "WBMMS NEXT", _id)
            _render_question(bot, session, question_id)
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

