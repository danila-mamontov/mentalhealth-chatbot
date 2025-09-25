import telebot
from survey import keycap_numbers, get_phq9_question_and_options, get_main_question
from utils.menu import phq9_menu, survey_menu
from handlers.main_survey_handler import get_controls_placeholder
from utils.storage import context, get_translation
from utils.logger import logger
from states import SurveyStates
from survey import get_phq9_total_questions


def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("answer_"),
                                state=SurveyStates.phq9)
    def handle_answer_button_response(call):
        t_id = call.message.chat.id
        message_id = call.message.message_id
        _, _, answer_number = call.data.split("_")

        answer_number = int(answer_number)
        with bot.retrieve_data(t_id, call.message.chat.id) as data:
            question_index = data.get("phq_index", 0)
            next_question_index = question_index + 1
            data["phq_index"] = next_question_index

        # Handle attention-check mapping
        attn_idx = context.get_user_info_field(t_id, "phq_attention_index")
        expected = context.get_user_info_field(t_id, "phq_attention_expected") or 1
        if attn_idx is not None and question_index == attn_idx:
            # this screen is attention check
            failed = 0 if answer_number == expected else 1
            context.set_user_info_field(t_id, "phq_attention_failed", failed)
        else:
            # map to real PHQ item index
            real_index = question_index
            if attn_idx is not None and question_index > attn_idx:
                real_index = question_index - 1
            context.set_user_info_field(t_id, f"phq_{real_index}", answer_number)

        logger.log_event(t_id, f"PHQ9 QUESTION {question_index}", f"answer {answer_number}")

        total = get_phq9_total_questions(t_id)
        if next_question_index < total:
            question, options = get_phq9_question_and_options(next_question_index, t_id)

            bot.edit_message_text(
                chat_id=t_id,
                message_id=message_id,
                text=get_translation(t_id, "starting_phq9_msg") +
                f"\n\n{keycap_numbers[next_question_index+1]}\t<b>{question}</b>",
                parse_mode="HTML",
                reply_markup=phq9_menu(next_question_index, options),
            )
        else:
            context.save_phq_info(t_id)

            logger.log_event(t_id, "END PHQ9 SURVEY")

            bot.delete_message(t_id, context.get_user_info_field(t_id, "message_to_del"))
            bot.edit_message_text(
                chat_id=t_id,
                message_id=message_id,
                text=get_translation(t_id, "intro_main_msg"),
                parse_mode="HTML",
            )

            sent_q = bot.send_message(
                chat_id=t_id,
                text=f"{keycap_numbers[1]}\t" + get_main_question(question_id=0, user_id=t_id),
                parse_mode="HTML",
            )
            sent_controls = bot.send_message(
                chat_id=t_id,
                text=get_controls_placeholder(t_id),
                parse_mode="HTML",
                reply_markup=survey_menu(t_id, question_index=0, voice_count=0),
            )

            context.set_user_info_field(t_id, "survey_message_id", sent_q.message_id)
            context.set_user_info_field(t_id, "survey_controls_id", sent_controls.message_id)
            context.set_user_info_field(t_id, "message_to_del", message_id)
            bot.set_state(t_id, SurveyStates.main, call.message.chat.id)
