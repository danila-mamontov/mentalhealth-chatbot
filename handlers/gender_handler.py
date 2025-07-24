import telebot
from utils.menu import age_range_menu, gender_menu, profile_menu
from utils.storage import context, get_user_profile, get_translation
from utils.logger import logger
from states import SurveyStates, EditProfileStates
def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(
        func=lambda call: call.data in ("male", "female", "noanswer", "set_gender_change"),
        state="*",
    )
    def handle_gender_selection(call):
        t_id = call.message.chat.id
        if call.data != "set_gender_change":
            gender = call.data
            context.set_user_info_field(t_id, "gender", gender)
            context.save_user_info(t_id)
            logger.log_event(t_id, "SET GENDER", gender)
            state = bot.get_state(t_id)
            if state == str(SurveyStates.gender) and not context.get_user_info_field(t_id, "age"):
                bot.set_state(t_id, SurveyStates.age, call.message.chat.id)
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=get_translation(t_id, "age_selection"),
                    parse_mode="HTML",
                    reply_markup=age_range_menu(t_id),
                )
            else:
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=get_user_profile(t_id),
                    parse_mode='HTML',
                    reply_markup=profile_menu(t_id),
                )
                bot.set_state(t_id, SurveyStates.main_menu, call.message.chat.id)

        else:
            logger.log_event(t_id, "CHANGE GENDER", "")
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=get_translation(t_id, "gender_selection"),
                parse_mode='HTML',
                reply_markup=gender_menu(t_id),
            )
            bot.set_state(t_id, EditProfileStates.gender, call.message.chat.id)





