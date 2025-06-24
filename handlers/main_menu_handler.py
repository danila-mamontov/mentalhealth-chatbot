import telebot
from survey import get_phq9_question_and_options, keycap_numbers
from utils.menu import (
    survey_menu,
    phq9_menu,
    consent_menu,
    gender_menu,
    age_range_menu,
)
from utils.storage import context, get_translation
from utils.logger import logger
from states import SurveyStates

def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("menu_"))
    def handle_menu_buttons(call):
        user_id = call.message.chat.id
        message_id = call.message.message_id
        if call.data == "menu_start_phq9_survey":
            if not context.get_user_info_field(user_id, "consent"):
                bot.set_state(user_id, SurveyStates.consent, call.message.chat.id)
                bot.edit_message_text(
                    chat_id=user_id,
                    message_id=message_id,
                    text=get_translation(user_id, "consent_message"),
                    parse_mode="HTML",
                    reply_markup=consent_menu(user_id),
                )
                return
            if not context.get_user_info_field(user_id, "gender"):
                bot.set_state(user_id, SurveyStates.gender, call.message.chat.id)
                bot.edit_message_text(
                    chat_id=user_id,
                    message_id=message_id,
                    text=get_translation(user_id, "gender_selection"),
                    parse_mode="HTML",
                    reply_markup=gender_menu(user_id),
                )
                return
            if not context.get_user_info_field(user_id, "age"):
                bot.set_state(user_id, SurveyStates.age, call.message.chat.id)
                bot.edit_message_text(
                    chat_id=user_id,
                    message_id=message_id,
                    text=get_translation(user_id, "age_selection"),
                    parse_mode="HTML",
                    reply_markup=age_range_menu(user_id),
                )
                return

            question, options = get_phq9_question_and_options(0, user_id)

            context.set_user_info_field(user_id, "message_to_del", message_id)

            logger.log_event(user_id, "START PHQ9 SURVEY")
            bot.edit_message_text(
                chat_id=user_id,
                message_id=message_id,
                text=get_translation(user_id, "intro_phq9_message"),
                parse_mode="HTML",
            )

            bot.set_state(user_id, SurveyStates.phq9, call.message.chat.id)
            with bot.retrieve_data(user_id, call.message.chat.id) as data:
                data["phq_index"] = 0

            bot.send_message(
                chat_id=user_id,
                text=get_translation(user_id, "starting_phq9")
                + f"\n\n{keycap_numbers[1]}\t<b>{question}</b>",
                parse_mode="HTML",
                reply_markup=phq9_menu(0, options),
            )

            # ask_phq9_question(bot, user_id)
        else:
            pass



