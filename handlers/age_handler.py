import telebot

from survey import get_phq9_question_and_options, keycap_numbers
from utils.chat_control import message_ids
from utils.menu import main_menu, exact_age_menu, age_range_menu, phq9_menu
from utils.storage import context, get_translation
from utils.logger import logger
from states import SurveyStates

def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("range_"), state=SurveyStates.age)
    def handle_age_range_selection(call):
        user_id = call.message.chat.id
        if "change" not in call.data:
            selected_range = call.data.split("_")[1]
            start_age, end_age = map(int, selected_range.split("-"))

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=get_translation(user_id, "age_selection"),
                reply_markup=exact_age_menu(user_id,start_age, end_age)
            )
        else:
            logger.log_event(user_id, "CHANGE AGE", "")
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=get_translation(user_id, "age_selection"),
                reply_markup=age_range_menu(user_id)
            )
            bot.set_state(user_id, SurveyStates.age, call.message.chat.id)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("age_"), state=SurveyStates.age)
    def handle_exact_age_selection(call):
        user_id = call.message.chat.id
        message_id = call.message.message_id
        selected_age = call.data.split("_")[1]

        context.set_user_info_field(user_id, "age", int(selected_age))
        context.save_user_info(user_id)
        logger.log_event(user_id, "SET AGE", selected_age)

        context.set_user_info_field(user_id, "current_question_index", 0)
        question, options = get_phq9_question_and_options(0, user_id)

        context.set_user_info_field(user_id, "message_to_del", message_id)

        logger.log_event(user_id, "START PHQ9 SURVEY")
        # bot.edit_message_text(chat_id=user_id,
        #                       message_id=message_id,
        #                       text=get_translation(user_id, 'intro_phq9_message'),
        #                       parse_mode='HTML')
        #
        # bot.send_message(chat_id=user_id,
        #                  text=get_translation(user_id,
        #                                       'starting_phq9') + f"\n{keycap_numbers[1]}\t" + f"<i><b>{question}</b></i>",
        #                  parse_mode='HTML',
        #                  reply_markup=phq9_menu(0, options))

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=get_translation(user_id, "main_menu_message"),
            parse_mode='HTML',
            reply_markup=main_menu(user_id)
        )
        bot.set_state(user_id, SurveyStates.main_menu, call.message.chat.id)

