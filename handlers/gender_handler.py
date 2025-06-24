import telebot
from utils.menu import age_range_menu, gender_menu, profile_menu
from utils.storage import context, get_user_profile, get_translation
from utils.logger import logger
from states import SurveyStates
def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(
        func=lambda call: call.data in ("male", "female", "noanswer", "set_gender_change"),
        state="*",
    )
    def handle_gender_selection(call):
        user_id = call.message.chat.id
        if call.data != "set_gender_change":
            gender = call.data
            context.set_user_info_field(user_id,"gender",gender)
            context.save_user_info(user_id)
            logger.log_event(user_id, "SET GENDER",gender)
            if not context.get_user_info_field(user_id, "age"):
                bot.set_state(user_id, SurveyStates.age, call.message.chat.id)
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text=get_translation(user_id, "age_selection"),
                                      parse_mode="HTML",
                                      reply_markup=age_range_menu(user_id))
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
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=get_translation(user_id, "gender_selection"),
                                  parse_mode='HTML',
                                  reply_markup=gender_menu(user_id))
            bot.set_state(user_id, SurveyStates.gender, call.message.chat.id)





