import telebot
from telebot.types import CallbackQuery
from states import SurveyStates

from utils.storage import context, get_user_profile, get_translation
from utils.menu import consent_menu, language_menu, profile_menu
from utils.logger import logger


# Handler for language selection buttons
def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(
        func=lambda call: call.data in ("en", "de", "ru", "set_language_change"),
        state="*",
    )
    def handle_language_selection(call):
        user_id = call.message.chat.id
        message_id = call.message.message_id
        language = call.data

        if language != "set_language_change":
            context.set_user_info_field(user_id, "language", language)
            context.save_user_info(user_id)
            logger.log_event(user_id, "SET LANGUAGE", language)
            if bot.get_state(user_id) == str(SurveyStates.language):
                bot.set_state(user_id, SurveyStates.consent, call.message.chat.id)
                bot.edit_message_text(chat_id=user_id,
                                      message_id=message_id,
                                      text=get_translation(user_id, "consent_message"),
                                      parse_mode='HTML',
                                      reply_markup=consent_menu(user_id))
            else:
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=get_user_profile(user_id),
                    parse_mode='HTML',
                    reply_markup=profile_menu(user_id),
                )
        else:
            logger.log_event(user_id, "CHANGE LANGUAGE", "")
            bot.edit_message_text(chat_id=user_id,
                                  message_id=message_id,
                                  text=get_translation(user_id, "language_selection"),
                                  parse_mode='HTML',
                                  reply_markup=language_menu())
            bot.set_state(user_id, SurveyStates.language, call.message.chat.id)

