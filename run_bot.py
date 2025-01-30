import telebot
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import pandas as pd
from survey import phq9_survey, main_survey, emoji_mapping
from localization import translations

# Читаем токен из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")
# Replace with your bot's token
bot = telebot.TeleBot(TOKEN)

phq9_user_answers = pd.DataFrame(columns=['user_id','language']+list(phq9_survey['en'].keys()))
current_question_index = {}
user_survey_progress = {}
responses_dir = "responses"
if not os.path.exists(responses_dir):
    os.makedirs(responses_dir)

message_ids = {}
def update_message_ids(chat_id, message_id):
    if chat_id in message_ids.keys():
        message_ids[chat_id].append(message_id)
    else:
        message_ids[chat_id] = [message_id]
    return
def delete_last_n_message(chat_id, n):
    try:
        bot.delete_message(chat_id, message_ids[chat_id][-n])
        message_ids[chat_id].pop()
    except:
        pass
    return

# Function to get the translation for the current language
def get_translation(user_id,key):
    user_data = phq9_user_answers.loc[phq9_user_answers['user_id'] == user_id]
    language = user_data.iloc[-1]['language'] if not user_data.empty else "en"
    return translations[language].get(key, key)

# Handler for the /start command
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.chat.id
    if user_id not in current_question_index:
        current_question_index[user_id] = 0
    # Initialize user's language and current question index
    phq9_user_answers.loc[len(phq9_user_answers)] = [user_id, 'en'] + [None] * (len(phq9_user_answers.columns) - 2)

    if not os.path.exists(os.path.join(responses_dir, f"{user_id}")):
        os.makedirs(os.path.join(responses_dir, f"{user_id}", "audio"))

    # Send language selection menu
    bot.send_message(user_id, 'Please choose your language:', reply_markup=language_menu())
# Main menu
def main_menu(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(get_translation(user_id, 'phq9_survey_button'), callback_data="menu_start_phq9_survey"),
                InlineKeyboardButton(get_translation(user_id,'main_survey_button'), callback_data="menu_start_main_survey"))
    return markup
# Handler for menu buttons
@bot.callback_query_handler(func=lambda call: call.data.startswith("menu_"))
def handle_menu_buttons(call):
    user_id = call.message.chat.id
    if call.data == "menu_start_phq9_survey":
        current_question_index[user_id] = 0
        bot.send_message(user_id, get_translation(user_id, 'starting_phq9'), parse_mode='HTML')
        ask_next_question(user_id)
    elif call.data == "menu_start_main_survey":
        user_id = call.message.chat.id
        bot.send_message(user_id, get_translation(user_id, 'starting_main_survey'), parse_mode='HTML')
        ask_next_main_question(user_id)
    else:
        bot.send_message(user_id, "Invalid option selected.")
    # Remove buttons after clicking
    try:
        bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=None)
    except Exception as e:
        print(f"Error while removing reply markup: {e}")
def language_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("Continue in English", callback_data="set_language_en"),
               InlineKeyboardButton("Weiter auf Deutsch", callback_data="set_language_de"),
               InlineKeyboardButton("Продолжить на Русском", callback_data="set_language_ru"))
    return markup
# Function to ask the next question
def ask_next_question(user_id):
    index = current_question_index.get(user_id, 0)
    user_data = phq9_user_answers
    user_row = user_data.loc[user_data['user_id'] == user_id]
    if not user_row.empty:
        language = user_row.iloc[-1]['language']
        content = phq9_survey

        if index < len(content[language]):
            question = list(content[language].keys())[index]
            options = content[language].get(question)
            markup = InlineKeyboardMarkup()
            if options:
                for i, option in enumerate(options):
                    markup.add(InlineKeyboardButton(emoji_mapping[i+1]+'\t'+option, callback_data=f"answer_{option}"))
            bot.send_message(user_id, question, reply_markup=markup,parse_mode='HTML')
        else:
            bot.send_message(user_id, get_translation(user_id, "end_phq9_message"))
            save_answers(user_id)
# Handler for language selection buttons
@bot.callback_query_handler(func=lambda call: call.data.startswith("set_language_"))
def handle_language_selection(call):
    user_id = call.message.chat.id
    language = call.data.split("_")[2]

    # Save user's language choice
    user_survey_progress[user_id] = {"index": 0, "language": language}

    user_rows = phq9_user_answers.loc[phq9_user_answers['user_id'] == user_id]
    if not user_rows.empty:
        last_index = user_rows.index[-1]
        phq9_user_answers.loc[last_index, 'language'] = language
    # Send confirmation message in selected language
    bot.send_message(user_id, get_translation(user_id,'start_message'), reply_markup=main_menu(user_id))

    # Remove last message
    update_message_ids(user_id, call.message.message_id)
    delete_last_n_message(user_id, 1)
    # Remove language selection buttons after they are clicked
    try:
        bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=None)
    except Exception as e:
        print(f"Error while removing reply markup: {e}")

# Handle inline button responses
@bot.callback_query_handler(func=lambda call: call.data.startswith("answer_"))
def handle_button_response(call):
    user_id = call.message.chat.id
    _, answer = call.data.split("_", 1)

    user_data = phq9_user_answers
    index = current_question_index.get(user_id, 0)

    if index < len(phq9_survey['en']):
        question = list(phq9_survey['en'].keys())[index]
        last_index = user_data[user_data['user_id'] == user_id].index[-1]
        language = user_data.at[last_index, 'language']
        answer_index = list(phq9_survey[language].values())[index].index(answer)
        user_data.at[last_index, question] = list(phq9_survey['en'].values())[index][answer_index]
        bot.send_message(user_id, get_translation(user_id, 'your_answer') + answer + "\n--------------------------------")
        current_question_index[user_id] += 1
        ask_next_question(user_id)
    bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=None)

def ask_next_main_question(user_id):
    progress = user_survey_progress.get(user_id)
    if not progress:
        return

    language = progress["language"]
    index = progress["index"]
    questions = list(main_survey[language].keys())

    if index < len(questions):
        bot.send_message(user_id, questions[index])
    else:
        bot.send_message(user_id, get_translation(language, "end_main_survey"))
        user_survey_progress.pop(user_id, None)

@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    user_id = message.chat.id
    if user_id not in user_survey_progress:
        bot.send_message(user_id, get_translation(user_id, "voice_out_of_survey"))
        return

    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_path = os.path.join(responses_dir,f"{user_id}","audio", f"{user_id}_{user_survey_progress[user_id]['index']}.ogg")
    with open(file_path, 'wb') as f:
        f.write(downloaded_file)

    user_survey_progress[user_id]['index'] += 1
    ask_next_main_question(user_id)


# Save user's answers
def save_answers(user_id):
    user_data = phq9_user_answers
    save_path = os.path.join(responses_dir,f"{user_id}", f"{user_id}_PHQ9.csv")
    user_data.to_csv(save_path, mode='a', header=not user_data.empty, index=False)
    bot.send_message(user_id, get_translation(user_id, "answer_confirmation"))

    bot.send_message(user_id, get_translation(user_id, "main_menu_message"), reply_markup=main_menu(user_id))
# Run the bot
if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()