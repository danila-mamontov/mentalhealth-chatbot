import telebot
from survey import get_phq9_question_and_options, keycap_numbers, get_main_question
from utils.menu import phq9_menu, yes_no_menu, survey_menu
from utils.storage import context, get_translation, get_survey_progress, get_first_unanswered_question
from utils.logger import logger
from states import SurveyStates
from survey import phq9_survey
from survey_session import SurveyManager
from handlers.main_survey_handler import get_controls_placeholder

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
            # Delete welcome message if it exists
            welcome_msg_id = context.get_user_info_field(t_id, "welcome_message_id")
            if welcome_msg_id:
                try:
                    bot.delete_message(t_id, welcome_msg_id)
                except Exception:
                    pass
                context.set_user_info_field(t_id, "welcome_message_id", None)

            # Check if user already has survey progress
            user_id = context.get_user_info_field(t_id, "id")
            if user_id:
                progress = get_survey_progress(user_id)
                next_stage = progress.get('next_stage')

                # If user already completed PHQ9, redirect to next incomplete stage
                if next_stage and next_stage != 'phq9':
                    logger.log_event(t_id, "RESUME SURVEY", f"next_stage={next_stage}")

                    if next_stage == 'main_survey':
                        # Resume main voice survey
                        session = SurveyManager.get_session(t_id)

                        # Get first unanswered question
                        first_unanswered = get_first_unanswered_question(user_id)
                        session.jump_to(first_unanswered)

                        context.set_user_info_field(t_id, "message_to_del", message_id)

                        # Show first unanswered question
                        question_num = first_unanswered + 1
                        if question_num <= 9:
                            keycap = keycap_numbers[question_num]
                        else:
                            keycap = keycap_numbers[question_num // 10] + keycap_numbers[question_num % 10 + 1]

                        bot.edit_message_text(
                            chat_id=t_id,
                            message_id=message_id,
                            text=f"{keycap}\t" + get_main_question(question_id=first_unanswered, user_id=t_id),
                            parse_mode="HTML",
                        )

                        sent_controls = bot.send_message(
                            chat_id=t_id,
                            text=get_controls_placeholder(t_id),
                            parse_mode="HTML",
                            reply_markup=survey_menu(t_id, question_index=first_unanswered, voice_count=0),
                        )

                        context.set_user_info_field(t_id, "survey_message_id", message_id)
                        context.set_user_info_field(t_id, "survey_controls_id", sent_controls.message_id)
                        bot.set_state(t_id, SurveyStates.main, t_id)
                        return

                    if next_stage == 'depressive':
                        bot.edit_message_text(
                            chat_id=t_id,
                            message_id=message_id,
                            text=get_translation(t_id, "depressive_feelings_msg"),
                            parse_mode="HTML",
                            reply_markup=yes_no_menu(t_id),
                        )
                        bot.set_state(t_id, SurveyStates.depressive, t_id)
                        return

                    elif next_stage == 'treatment':
                        bot.edit_message_text(
                            chat_id=t_id,
                            message_id=message_id,
                            text=get_translation(t_id, "treatment_selection_msg"),
                            parse_mode="HTML",
                            reply_markup=yes_no_menu(t_id),
                        )
                        bot.set_state(t_id, SurveyStates.treatment, t_id)
                        return

                    elif next_stage == 'reading_text':
                        reading_text_intro = get_translation(t_id, "reading_text_intro_msg")
                        reading_text_content = get_translation(t_id, "reading_text_content_msg")
                        reading_text_instruction = get_translation(t_id, "reading_text_instruction_msg")
                        confirmation_msg = get_translation(t_id, "reading_text_confirm_msg")

                        full_msg = reading_text_intro + "\n\n" + reading_text_content + "\n\n" + reading_text_instruction + "\n\n" + confirmation_msg

                        from utils.menu import confirm_menu

                        bot.edit_message_text(
                            chat_id=t_id,
                            message_id=message_id,
                            text=full_msg,
                            parse_mode="HTML",
                            reply_markup=confirm_menu(t_id),
                        )
                        context.set_user_info_field(t_id, "message_to_del", message_id)
                        context.set_user_info_field(t_id, "reading_text_confirm_msg_id", message_id)
                        context.set_user_info_field(t_id, "reading_text_total_duration", 0)
                        bot.set_state(t_id, SurveyStates.reading_text_confirm, t_id)
                        return
                        return

                    elif next_stage == 'final_menu':
                        from utils.menu import final_menu
                        final_menu_msg = get_translation(t_id, "final_menu_msg").format(user_id=user_id)
                        end_survey_msg = get_translation(t_id, "end_main_survey_msg").format(user_id=user_id)
                        menu_msg = end_survey_msg + "\n\n" + final_menu_msg

                        bot.edit_message_text(
                            chat_id=t_id,
                            message_id=message_id,
                            text=menu_msg,
                            parse_mode="HTML",
                            reply_markup=final_menu(t_id),
                        )
                        bot.set_state(t_id, SurveyStates.final_menu, t_id)
                        return

            # User is starting fresh - initialize PHQ9 survey
            # initialize one attention-check per survey run
            lang = context.get_user_info_field(t_id, "language") or "en"
            base_count = len(phq9_survey[lang])
            attn_idx = 5  # insert at random position
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
