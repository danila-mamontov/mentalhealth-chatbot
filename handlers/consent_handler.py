import telebot
from states import SurveyStates
from utils.menu import gender_menu, profile_menu
from utils.logger import logger
from utils.storage import context, get_user_profile, get_translation

def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data in ("yes", "no"), state=SurveyStates.consent)
    def handle_consent(call):
        t_id = call.message.chat.id
        message_id = call.message.message_id
        if call.data == "yes":
            # bot.send_message(t_id, get_translation(t_id,"consent_yes"))
            context.set_user_info_field(t_id, "consent", "yes")
            context.save_user_info(t_id)
            logger.log_event(t_id, "SET CONSENT", "YES")
            bot.set_state(t_id, SurveyStates.gender, call.message.chat.id)
            bot.edit_message_text(chat_id=t_id,
                                  message_id=message_id,
                                  text=get_translation(t_id, "gender_selection"),
                                  parse_mode='HTML',
                                  reply_markup=gender_menu(t_id))


            # ask_phq9_question(bot, t_id)
        elif call.data == "no":
            context.set_user_info_field(t_id, "consent", "no")
            context.save_user_info(t_id)
            logger.log_event(t_id, "SET CONSENT", "NO")
            bot.delete_state(t_id)
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=message_id,
                                  text=get_translation(t_id, "consent_no"),
                                  parse_mode='HTML',
                                  reply_markup=None)
        # bot.edit_message_reply_markup(t_id, call.message.message_id, reply_markup=None)


