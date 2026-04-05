import telebot
from survey import get_main_question,get_phq9_question_and_options, keycap_numbers
from utils.menu import survey_menu, phq9_menu, yes_no_menu
from handlers.main_survey_handler import get_controls_placeholder
from utils.storage import context, get_translation
from utils.logger import logger
from states import SurveyStates
from survey import phq9_survey

def register_handlers(bot: telebot.TeleBot):
    @bot.message_handler(commands=['test_skip'])
    def handle_test_skip_command(message: telebot.types.Message):
        """Skip main survey and go directly to depressive question for testing."""
        t_id = message.chat.id
        logger.log_event(t_id, "TEST SKIP SURVEY", "started")

        # Send depressive question directly
        bot.send_message(
            t_id,
            get_translation(t_id, "depressive_feelings_msg"),
            parse_mode="HTML",
            reply_markup=yes_no_menu(t_id),
        )
        bot.set_state(t_id, SurveyStates.depressive, t_id)

    @bot.message_handler(commands=['test_last'])
    def handle_test_last_command(message: telebot.types.Message):
        """Skip everything and go directly to reading text stage for testing."""
        t_id = message.chat.id
        logger.log_event(t_id, "TEST SKIP TO READING TEXT", "started")

        # Set dummy values for depressive and treatment
        context.set_user_info_field(t_id, "depressive", "yes")
        context.set_user_info_field(t_id, "treatment", "yes")
        context.save_user_info(t_id)

        # Send reading text intro and content
        reading_text_intro = get_translation(t_id, "reading_text_intro_msg")
        reading_text_content = get_translation(t_id, "reading_text_content_msg")
        reading_text_instruction = get_translation(t_id, "reading_text_instruction_msg")

        bot.send_message(
            t_id,
            reading_text_intro + "\n\n" + reading_text_content + "\n\n" + reading_text_instruction,
            parse_mode="HTML",
        )
        bot.set_state(t_id, SurveyStates.reading_text, t_id)

    # ...existing code...
    @bot.callback_query_handler(func=lambda call: call.data.startswith("menu_"))
    def handle_menu_buttons(call):
        t_id = call.message.chat.id
        message_id = call.message.message_id
        if call.data == "menu_start_phq9_survey":
            # initialize one attention-check per survey run
            lang = context.get_user_info_field(t_id, "language") or "en"
            base_count = len(phq9_survey[lang])
            attn_idx = 5 #randint(0, base_count)   inclusive range -> insert at random position
            context.set_user_info_field(t_id, "phq_attention_index", attn_idx)
            context.set_user_info_field(t_id, "phq_attention_expected", 3)  # expect option '2' (0-based index 1)
            context.set_user_info_field(t_id, "phq_attention_failed", 0)

            question, options = get_phq9_question_and_options(0, t_id)

            context.set_user_info_field(t_id, "message_to_del", message_id)

            logger.log_event(t_id, "START PHQ9 SURVEY")
            bot.edit_message_text(chat_id=t_id,
                                  message_id=message_id,
                                  text=get_translation(t_id, 'intro_phq9_msg'),
                                  parse_mode='HTML')

            bot.set_state(t_id, SurveyStates.phq9, call.message.chat.id)
            with bot.retrieve_data(t_id, call.message.chat.id) as data:
                data["phq_index"] = 0

            bot.send_message(
                chat_id=t_id,
                text=get_translation(t_id, 'starting_phq9_msg') +
                f"\n\n{keycap_numbers[1]}\t<b>{question}</b>",
                parse_mode='HTML',
                reply_markup=phq9_menu(0, options),
            )

            # ask_phq9_question(bot, t_id)
        elif call.data == "menu_start_main_survey":
            context.set_user_info_field(t_id, "message_to_del", message_id)

            logger.log_event(t_id, "START MAIN SURVEY")
            bot.edit_message_text(chat_id=t_id,
                                  message_id=message_id,
                                  text=get_translation(t_id, 'intro_main_msg'),
                                  parse_mode='HTML')

            bot.set_state(t_id, SurveyStates.main, call.message.chat.id)
            with bot.retrieve_data(t_id, call.message.chat.id) as data:
                data["main_index"] = 0

            sent_q = bot.send_message(
                chat_id=t_id,
                text=f"{keycap_numbers[1]}\t" + get_main_question(question_id=0, user_id=t_id),
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
