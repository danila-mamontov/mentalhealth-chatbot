import telebot
from survey import keycap_numbers, get_phq9_question_and_options
from utils.menu import phq9_menu, main_menu
from utils.storage import context
from localization import get_translation


# Function to ask the next question
# def ask_next_phq9_question(bot, user_id):
#     index = context.get_user_info_field(user_id, "current_question_index")
#
#     if index < len(phq9_survey['en']):
#         question, options = get_phq9_question_and_options(index, user_id)
#         keycap_number = keycap_numbers[(index+1)]
#         bot.send_message(user_id,f"{keycap_numbers[(index+1)]}\t"+f"<i><b>{question}</b></i>",
#                          reply_markup=phq9_menu(user_id, index, options),
#                          parse_mode='HTML')
#     else:
#         bot.send_message(user_id, get_translation(user_id, "end_phq9_message"))
#         bot.send_message(user_id, get_translation(user_id, 'starting_main_survey'), parse_mode='HTML')

def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("answer_"))
    def handle_answer_button_response(call):
        user_id = call.message.chat.id
        _, question_index, answer_number= call.data.split("_")

        question_index = int(question_index)
        answer_number = int(answer_number)
        next_question_index = question_index + 1

        context.set_user_info_field(user_id, f"phq9_{question_index}", answer_number)
        context.set_user_info_field(user_id, "current_question_index", next_question_index)

        if next_question_index < 9:
            question, options = get_phq9_question_and_options(next_question_index, user_id)

            bot.edit_message_text(chat_id=user_id,
                                  message_id=call.message.message_id,
                                  text=get_translation(user_id, 'starting_phq9')+f"\n{keycap_numbers[next_question_index+1]}\t"+f"<i><b>{question}</b></i>",
                                  reply_markup=phq9_menu(next_question_index, options),
                                  parse_mode='HTML')

            # ask_next_phq9_question(bot, user_id)
        else:
            context.save_phq9_info(user_id)
            context.set_user_info_field(user_id, "current_question_index", 0)

            bot.edit_message_text(chat_id=user_id,
                                  message_id=call.message.message_id,
                                  text=get_translation(user_id, "end_phq9_message")+"\n\n"+get_translation(user_id, 'main_menu_message'),
                                  parse_mode='HTML',
                                  reply_markup=main_menu(user_id))
