import telebot
from survey import keycap_numbers, get_phq9_question_and_options, get_wbmms_question
from utils.menu import phq9_menu, survey_menu
from handlers.wbmms_survey_handler import CONTROL_PLACEHOLDER
from utils.storage import context, get_translation
from utils.logger import logger
from states import SurveyStates


def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("answer_"),
                                state=SurveyStates.phq9)
    def handle_answer_button_response(call):
        user_id = call.message.chat.id
        message_id = call.message.message_id
        _, _, answer_number = call.data.split("_")

        answer_number = int(answer_number)
        with bot.retrieve_data(user_id, call.message.chat.id) as data:
            question_index = data.get("phq_index", 0)
            next_question_index = question_index + 1
            data["phq_index"] = next_question_index

        context.set_user_info_field(user_id, f"phq_{question_index}", answer_number)

        logger.log_event(user_id, f"PHQ9 QUESTION {question_index}", f"answer {answer_number}")
        if next_question_index < 8:
            question, options = get_phq9_question_and_options(next_question_index, user_id)

            bot.edit_message_text(
                chat_id=user_id,
                message_id=message_id,
                text=get_translation(user_id, "starting_phq9") +
                f"\n\n{keycap_numbers[next_question_index+1]}\t<b>{question}</b>",
                parse_mode="HTML",
                reply_markup=phq9_menu(next_question_index, options),
            )
        else:
            context.save_phq_info(user_id)

            logger.log_event(user_id, "END PHQ9 SURVEY")

            bot.delete_message(user_id, context.get_user_info_field(user_id, "message_to_del"))
            bot.edit_message_text(
                chat_id=user_id,
                message_id=message_id,
                text=get_translation(user_id, "intro_main_message"),
                parse_mode="HTML",
            )

            sent_q = bot.send_message(
                chat_id=user_id,
                text=f"{keycap_numbers[1]}\t" + get_wbmms_question(question_id=0, user_id=user_id),
                parse_mode="HTML",
            )
            sent_controls = bot.send_message(
                chat_id=user_id,
                text=CONTROL_PLACEHOLDER,
                parse_mode="HTML",
                reply_markup=survey_menu(user_id, question_index=0),
            )

            context.set_user_info_field(user_id, "survey_message_id", sent_q.message_id)
            context.set_user_info_field(user_id, "survey_controls_id", sent_controls.message_id)
            context.set_user_info_field(user_id, "message_to_del", message_id)
            bot.set_state(user_id, SurveyStates.wbmms, call.message.chat.id)


