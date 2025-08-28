from __future__ import annotations
import telebot
from states import SurveyStates, EditProfileStates

from utils.storage import context, get_user_profile, get_translation
from utils.menu import consent_menu, language_menu, profile_menu
from localization import get_available_languages
from utils.logger import logger
from flow.renderer import render_node, engine


# Handler for language selection buttons
def register_handlers(bot: telebot.TeleBot):
    @bot.callback_query_handler(
        func=lambda call: call.data in get_available_languages() or call.data == "set_language_change",
        state=[SurveyStates.language,SurveyStates.language_confirm, EditProfileStates.editing_profile, EditProfileStates.language],
    )
    def handle_language_selection(call):
        t_id = call.message.chat.id
        message_id = call.message.message_id
        language = call.data
        state = bot.get_state(t_id)
        if state == SurveyStates.language.name:
            context.set_user_info_field(t_id, "language", language)
            context.save_user_info(t_id)
            logger.log_event(t_id, "SET LANGUAGE", language)
            # 1) Update the initial welcome message in-place
            welcome_mid = context.get_user_info_field(t_id, "welcome_message_id")
            if welcome_mid:
                render_node(bot, t_id, "welcome", message_id=welcome_mid)
            # 2) Turn the current language selection message into consent
            render_node(
                bot,
                t_id,
                engine.next("language") or "consent",
                message_id=message_id,
            )

        if state == SurveyStates.language_confirm:
            context.set_user_info_field(t_id, "language", language)
            context.save_user_info(t_id)
            logger.log_event(t_id, "SET LANGUAGE", language)

            render_node(bot, t_id, "consent", message_id=message_id)

        if state == EditProfileStates.editing_profile.name:
            logger.log_event(t_id, "CHANGE LANGUAGE", "")
            bot.set_state(t_id, EditProfileStates.language, call.message.chat.id)
            render_node(
                bot,
                t_id,
                "language_reselect",
                message_id=message_id,
                menu=lambda _tid: language_menu(),
            )


        elif state == EditProfileStates.language.name:
            context.set_user_info_field(t_id, "language", language)
            context.save_user_info(t_id)
            logger.log_event(t_id, "SET LANGUAGE", language)

            bot.set_state(t_id, EditProfileStates.editing_profile, call.message.chat.id)
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=get_user_profile(t_id),
                parse_mode='HTML',
                reply_markup=profile_menu(t_id),
            )


