import telebot
from telebot.types import CallbackQuery
from utils.menu import gender_menu, profile_menu
from utils.logger import logger
from utils.storage import context, get_user_profile, get_translation

def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("consent_"))
    def handle_consent(call: CallbackQuery):
        user_id = call.message.chat.id
        message_id = call.message.message_id
        if call.data == "consent_yes":
            # bot.send_message(user_id, get_translation(user_id,"consent_yes"))
            context.set_user_info_field(user_id, "consent", "yes")
            context.save_user_info(user_id)
            logger.log_event(user_id, "SET CONSENT", "YES")
            if not context.get_user_info_field(user_id,"gender"):
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=message_id,
                                      text=get_translation(user_id,"gender_selection"),
                                      parse_mode='HTML',
                                      reply_markup=gender_menu(user_id))
            else:
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=get_user_profile(user_id),
                    parse_mode='HTML',
                    reply_markup=profile_menu(user_id),
                )

            # ask_phq9_question(bot, user_id)
        elif call.data == "consent_no":
            context.set_user_info_field(user_id, "consent", "no")
            context.save_user_info(user_id)
            logger.log_event(user_id, "SET CONSENT", "NO")
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=message_id,
                                  text=get_translation(user_id,"consent_no"),
                                  parse_mode='HTML',
                                  reply_markup=None)
        # bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=None)
