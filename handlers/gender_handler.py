import telebot
from survey import get_phq9_question_and_options, keycap_numbers
from utils.menu import age_range_menu, gender_menu, profile_menu, phq9_menu
from utils.storage import context, get_user_profile, get_translation
from utils.logger import logger
from states import SurveyStates, EditProfileStates
def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(
        func=lambda call: call.data in ("male", "female", "noanswer", "set_gender_change"),
        state="*",
    )
    def handle_gender_selection(call):
        user_id = call.message.chat.id
        if call.data != "set_gender_change":
            gender = call.data
            context.set_user_info_field(user_id, "gender", gender)
            context.save_user_info(user_id)
            logger.log_event(user_id, "SET GENDER", gender)
            state = bot.get_state(user_id)
            if state == str(SurveyStates.gender) and not context.get_user_info_field(user_id, "age"):
                bot.set_state(user_id, SurveyStates.age, call.message.chat.id)
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=get_translation(user_id, "age_selection"),
                    parse_mode="HTML",
                    reply_markup=age_range_menu(user_id),
                )
            elif state == str(SurveyStates.gender):
                question, options = get_phq9_question_and_options(0, user_id)

                logger.log_event(user_id, "START PHQ9 SURVEY")
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=get_translation(user_id, "intro_phq9_message"),
                    parse_mode="HTML",
                )

                bot.set_state(user_id, SurveyStates.phq9, call.message.chat.id)
                with bot.retrieve_data(user_id, call.message.chat.id) as data:
                    data["phq_index"] = 0

                bot.send_message(
                    chat_id=call.message.chat.id,
                    text=get_translation(user_id, "starting_phq9")
                    + f"\n\n{keycap_numbers[1]}\t<b>{question}</b>",
                    parse_mode="HTML",
                    reply_markup=phq9_menu(0, options),
                )
            else:
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=get_user_profile(user_id),
                    parse_mode='HTML',
                    reply_markup=profile_menu(user_id),
                )
                bot.set_state(user_id, SurveyStates.main_menu, call.message.chat.id)

        else:
            logger.log_event(user_id, "CHANGE GENDER", "")
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=get_translation(user_id, "gender_selection"),
                parse_mode='HTML',
                reply_markup=gender_menu(user_id),
            )
            bot.set_state(user_id, EditProfileStates.gender, call.message.chat.id)





