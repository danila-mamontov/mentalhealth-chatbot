message_ids = {}
def update_message_ids(chat_id, message_id, message_caption:str):
    current_message = {message_caption: message_id}
    if chat_id in message_ids.keys():
        message_ids[chat_id].append(current_message)
    else:
        message_ids[chat_id] = [current_message]
    return
def delete_last_n_message(bot,chat_id, n):
    try:
        bot.delete_message(chat_id, message_ids[chat_id][-n])
        message_ids[chat_id].pop()
    except:
        pass
    return
