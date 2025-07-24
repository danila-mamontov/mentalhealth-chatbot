import telebot
from survey import get_wbmms_question,get_phq9_question_and_options, keycap_numbers
from utils.menu import survey_menu, phq9_menu
from handlers.wbmms_survey_handler import get_controls_placeholder
from utils.storage import context, get_translation
from utils.logger import logger
from states import SurveyStates

def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("menu_"))
    def handle_menu_buttons(call):
        t_id = call.message.chat.id
        message_id = call.message.message_id
        if call.data == "menu_start_phq9_survey":
            question, options = get_phq9_question_and_options(0, t_id)

            context.set_user_info_field(t_id, "message_to_del", message_id)

            logger.log_event(t_id, "START PHQ9 SURVEY")
            bot.edit_message_text(chat_id=t_id,
                                  message_id=message_id,
                                  text=get_translation(t_id, 'intro_phq9_message'),
                                  parse_mode='HTML')

            bot.set_state(t_id, SurveyStates.phq9, call.message.chat.id)
            with bot.retrieve_data(t_id, call.message.chat.id) as data:
                data["phq_index"] = 0

            bot.send_message(
                chat_id=t_id,
                text=get_translation(t_id, 'starting_phq9') +
                f"\n\n{keycap_numbers[1]}\t<b>{question}</b>",
                parse_mode='HTML',
                reply_markup=phq9_menu(0, options),
            )

            # ask_phq9_question(bot, t_id)
        elif call.data == "menu_start_main_survey":
            context.set_user_info_field(t_id, "message_to_del", message_id)

            logger.log_event(t_id, "START WBMMS SURVEY")
            bot.edit_message_text(chat_id=t_id,
                                  message_id=message_id,
                                  text=get_translation(t_id, 'intro_main_message'),
                                  parse_mode='HTML')
            bot.set_state(t_id, SurveyStates.wbmms, call.message.chat.id)
            with bot.retrieve_data(t_id, call.message.chat.id) as data:
                data["wbmms_index"] = 0

            sent_q = bot.send_message(
                chat_id=t_id,
                text=f"{keycap_numbers[1]}\t" + get_wbmms_question(question_id=0, user_id=t_id),
                parse_mode='HTML',
            )
            sent_controls = bot.send_message(
                chat_id=t_id,
                text=get_controls_placeholder(t_id),
                parse_mode='HTML',
                reply_markup=survey_menu(t_id, question_index=0, voice_count=0),
            )

            context.set_user_info_field(t_id, "survey_message_id", sent_q.message_id)
            context.set_user_info_field(t_id, "survey_controls_id", sent_controls.message_id)

        else:
            pass



