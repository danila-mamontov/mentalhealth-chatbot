import telebot
from survey import keycap_numbers, get_phq9_question_and_options, get_wbmms_question
from utils.menu import phq9_menu, main_menu, survey_menu
from utils.storage import context, get_translation
from utils.logger import logger


def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("answer_"))
    def handle_answer_button_response(call):
        user_id = call.message.chat.id
        message_id = call.message.message_id
        _, question_index, answer_number= call.data.split("_")

        question_index = int(question_index)
        answer_number = int(answer_number)
        next_question_index = question_index + 1

        context.set_user_info_field(user_id, f"phq_{question_index}", answer_number)
        context.set_user_info_field(user_id, "current_question_index", next_question_index)

        logger.log_event(user_id, f"PHQ9 QUESTION {question_index}", f"answer {answer_number}")
        if next_question_index < 8:
            question, options = get_phq9_question_and_options(next_question_index, user_id)

            bot.edit_message_text(chat_id=user_id,
                                  message_id=call.message.message_id,
                                  text=get_translation(user_id, 'starting_phq9')+f"\n\n{keycap_numbers[next_question_index+1]}\t"+f"<b>{question}</b>",
                                  parse_mode='HTML',
                                  reply_markup=phq9_menu(next_question_index, options)
                                  )

            # ask_next_phq9_question(bot, user_id)
        else:
            context.save_phq_info(user_id)
            context.set_user_info_field(user_id, "current_question_index", 0)

            logger.log_event(user_id, "END PHQ9 SURVEY")


            # bot.edit_message_text(chat_id=user_id,
            #                       message_id=call.message.message_id,
            #                       text=get_translation(user_id, "end_phq9_message")+"\n\n"+get_translation(user_id, 'main_menu_message'),
            #                       parse_mode='HTML',
            #                       reply_markup=main_menu(user_id))
            bot.delete_message(user_id, context.get_user_info_field(user_id, "message_to_del"))
            bot.edit_message_text(chat_id=user_id,
                                  message_id=message_id,
                                  text=get_translation(user_id, 'intro_main_message'),
                                  parse_mode='HTML')

            sent_message=bot.send_message(chat_id=user_id,
                             text=f"{keycap_numbers[1]}\t"+ get_wbmms_question(question_id=0,user_id=user_id),
                             parse_mode='HTML',
                             reply_markup=survey_menu(user_id, question_index=0))

            context.set_user_info_field(user_id, "survey_message_id", sent_message.message_id)

            context.set_user_info_field(user_id, "message_to_del", message_id)
