import telebot
from survey import get_phq9_question_and_options, keycap_numbers
from states import SurveyStates
from utils.menu import gender_menu, profile_menu, age_range_menu, phq9_menu
from utils.logger import logger
from utils.storage import context, get_user_profile, get_translation

def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data in ("yes", "no"), state=SurveyStates.consent)
    def handle_consent(call):
        user_id = call.message.chat.id
        message_id = call.message.message_id
        if call.data == "yes":
            # bot.send_message(user_id, get_translation(user_id,"consent_yes"))
            context.set_user_info_field(user_id, "consent", "yes")
            context.save_user_info(user_id)
            logger.log_event(user_id, "SET CONSENT", "YES")
            if not context.get_user_info_field(user_id, "gender"):
                bot.set_state(user_id, SurveyStates.gender, call.message.chat.id)
                bot.edit_message_text(
                    chat_id=user_id,
                    message_id=message_id,
                    text=get_translation(user_id, "gender_selection"),
                    parse_mode="HTML",
                    reply_markup=gender_menu(user_id),
                )
            elif not context.get_user_info_field(user_id, "age"):
                bot.set_state(user_id, SurveyStates.age, call.message.chat.id)
                bot.edit_message_text(
                    chat_id=user_id,
                    message_id=message_id,
                    text=get_translation(user_id, "age_selection"),
                    parse_mode="HTML",
                    reply_markup=age_range_menu(user_id),
                )
            else:
                question, options = get_phq9_question_and_options(0, user_id)

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
        elif call.data == "no":
            context.set_user_info_field(user_id, "consent", "no")
            context.save_user_info(user_id)
            logger.log_event(user_id, "SET CONSENT", "NO")
            bot.delete_state(user_id)
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=message_id,
                                  text=get_translation(user_id, "consent_no"),
                                  parse_mode='HTML',
                                  reply_markup=None)
        # bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=None)


