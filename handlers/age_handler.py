import telebot

from survey import get_phq9_question_and_options, keycap_numbers
from utils.chat_control import message_ids
from utils.menu import main_menu, exact_age_menu, age_range_menu, phq9_menu, profile_menu
from utils.storage import context, get_translation, get_user_profile
from utils.logger import logger
from states import SurveyStates, EditProfileStates
from flow.renderer import render_node, engine

def register_handlers(bot: telebot.TeleBot):
    _AGE_RANGES = {"18-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89", "90+"}

    @bot.callback_query_handler(
        func=lambda call, ranges=_AGE_RANGES: call.data in ranges or call.data == "range_change",
        state="*",
    )
    def handle_age_range_selection(call):
        t_id = call.message.chat.id
        if call.data != "range_change":
            selected_range = call.data
            if selected_range.endswith("+"):
                start_age = int(selected_range[:-1])
                end_age = start_age + 9
            else:
                start_age, end_age = map(int, selected_range.split("-"))

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=get_translation(t_id, "age_selection"),
                reply_markup=exact_age_menu(t_id,start_age, end_age)
            )
        else:
            logger.log_event(t_id, "CHANGE AGE", "")
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=get_translation(t_id, "age_selection"),
                reply_markup=age_range_menu(t_id)
            )
            current = bot.get_state(t_id)
            if current == str(SurveyStates.age):
                bot.set_state(t_id, SurveyStates.age, call.message.chat.id)
            else:
                bot.set_state(t_id, EditProfileStates.age, call.message.chat.id)

    @bot.callback_query_handler(func=lambda call: call.data.isdigit(), state="*")
    def handle_exact_age_selection(call):
        t_id = call.message.chat.id
        message_id = call.message.message_id
        selected_age = call.data

        context.set_user_info_field(t_id, "age", int(selected_age))
        context.save_user_info(t_id)
        logger.log_event(t_id, "SET AGE", selected_age)

        question, options = get_phq9_question_and_options(0, t_id)

        context.set_user_info_field(t_id, "message_to_del", message_id)

        state = bot.get_state(t_id)
        if state == str(SurveyStates.age):
            # linear transition to main menu via flow
            render_node(
                bot,
                t_id,
                engine.next("age") or "main_menu",
                message_id=call.message.message_id,
                menu=main_menu,
            )
        else:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=get_user_profile(t_id),
                parse_mode='HTML',
                reply_markup=profile_menu(t_id)
            )
            bot.set_state(t_id, SurveyStates.main_menu, call.message.chat.id)
