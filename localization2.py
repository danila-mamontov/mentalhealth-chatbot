from utils.storage import context
# Function to get the translation for the current language
def get_translation(user_id,key):
    language = context.get_user_info_field(user_id, "language")
    return translations[language].get(key, key)

translations = {
    'en': {
        'who_website': 'More Info about Depression',

        'help': 'Here are all available commands:\n'
                '/start - Start the bot\n'
                '/language - Change the language\n'
                '/help - Get help\n',

        'yes': 'Yes',
        'no': 'No',

        'previous': 'Previous',
        'next': 'Next',
        'finish_button': 'Finish the survey',

        'consent_message': 'All data collected will be anonymized and used for research purposes only. Do you consent to participate in the study?',
        'consent_yes': 'Thank you for your consent!',
        'consent_no': 'If you do not consent, you cannot participate in the study. If you change your mind, you can /start the survey again.',

        'gender_selection': 'Please select your gender:',
        'gender_male': 'male',
        'gender_female': 'female',
        'gender_other': 'no answer',

        'age_selection': 'Please choose your age:',

        'depression_diagnosis': 'Have you ever been diagnosed with a depressive disorder?',
        'depressive_feelings': 'Do you feel that you have had/have depression?',
        'treatment_selection': 'Do you take antidepressants currently or lately?',

        'welcome_message': "👋 Welcome!\n\n"
                         "This bot is part of a <b>scientific study</b> aimed at collecting data on people's emotional states.\n\n"
                         "⚠️ <b>Please note:</b> This bot <b>does not provide psychological support or counseling.</b>\n\n"
                         "❗ If at any point you feel discomfort, distress, or need support, we strongly recommend reaching out to professionals:\n"
                         "📞 <b>Support hotlines:</b> (provide relevant contacts)\n"
                         "🏥 <b>Professional help:</b> If you have concerns about your emotional well-being, consider consulting a psychologist or therapist.\n"
                         "👨‍👩‍👧‍👦 <b>Talk to close ones:</b> Sharing your feelings with trusted friends or family can be helpful.\n\n"
                         "✅ Participation is <b>completely voluntary</b>, and you can stop at any time by typing <b>/stop</b>.\n\n"
                         "🙏 Thank you for contributing to science!",

        'main_menu_message': 'Please choose an option:',
        'phq9_survey_button': "Start PHQ-9 Survey",
        'main_survey_button': "Start Main Survey",


        'end_phq9_message': 'Thank you for participating in the survey!',

        'answer_confirmation': 'Your answer has been recorded.',
        'age_validation_error': "Please enter a valid age (between 18 and 100).",
        'age_numeric_error': "Please enter a numeric value for age.",

        'intro_phq9_message': '📝 In this survey, you will be asked a series of questions about your mood, thoughts, and feelings. ',

        'question': 'Question #',
        'starting_phq9': "<b>Over the <u>last 2 weeks</u>, how often have you been bothered by any of the following problems?</b>",
        'your_answer': 'Your answer: ',
        'checkmark': '✔️',


        'intro_main_message': "📝 In this survey, we will ask you a series of questions about your thoughts, feelings, and experiences. "
                                 "These questions will help us better understand emotional well-being and how people experience their daily lives.\n\n"
                                 "💡 <b>What to expect?</b>\n"
                                 "✅ You will answer <b>14 simple questions</b> about your emotions, mood, and interactions with others.\n"
                                 "✅ You will respond to questions by <b>recording voice messages</b>.\n"
                                 "✅ There are no right or wrong answers—just share what feels true to you.\n"
                                 "✅ Your responses are <b>confidential</b> and used only for scientific research.\n\n"
                                 "⚠️ <b>Important:</b> This bot <b>does not provide psychological help</b>. If you feel uncomfortable, you can stop at any time by typing <b>/stop</b>. "
                                 "If you need support, please reach out to a professional.\n\n"
                                 "👉 When you're ready, let's begin!",

        'end_main_survey_message': 'Thank you for participating in the survey!',

        'voice_out_of_survey': 'You are currently not in a survey. Please start the main survey to answer questions.',
        'voice_recieved': 'Your voice message has been received. If you want to send another answer, please do so. Otherwise, you can proceed to the next or previous question.',
    },
    'de': {
        'who_website': 'Weitere Informationen zur Depression',

        'help': 'Hier sind alle verfügbaren Befehle:\n'
                '/start - Starten Sie den Bot\n'
                '/language - Ändern Sie die Sprache\n'
                '/help - Hilfe erhalten\n',

        'yes': 'Ja',
        'no': 'Nein',

        'previous': 'Zurück',
        'next': 'Weiter',
        'finish_button': 'Umfrage beenden',

        'consent_message': 'Alle gesammelten Daten werden anonymisiert und ausschließlich zu Forschungszwecken verwendet. Stimmen Sie der Teilnahme an der Studie zu?',
        'consent_yes': 'Vielen Dank für Ihre Zustimmung!',
        'consent_no': 'Wenn Sie nicht zustimmen, können Sie nicht an der Studie teilnehmen. Wenn Sie Ihre Meinung ändern, können Sie den Fragebogen erneut starten (/start).',

        'gender_selection': 'Bitte wählen Sie Ihr Geschlecht:',
        'gender_male': 'männlich',
        'gender_female': 'weiblich',
        'gender_other': 'keine Angabe',

        'age_selection': 'Bitte wählen Sie Ihr Alter:',

        'depression_diagnosis': 'Wurde bei Ihnen jemals eine depressive Störung diagnostiziert?',
        'depressive_feelings': 'Haben Sie das Gefühl, dass Sie eine Depression hatten/haben?',

        'treatment_selection': 'Nehmen Sie derzeit oder in letzter Zeit Antidepressiva ein?',

        'welcome_message': "👋 Willkommen!\n\n"
                         "Dieser Bot ist Teil einer <b>wissenschaftlichen Studie</b>, die darauf abzielt, Daten über die emotionalen Zustände von Menschen zu sammeln.\n\n"
                         "⚠️ <b>Bitte beachten Sie:</b> Dieser Bot <b>bietet keine psychologische Unterstützung oder Beratung.</b>\n\n"
                         "❗ Falls Sie sich während der Nutzung unwohl fühlen oder Unterstützung benötigen, empfehlen wir Ihnen, sich an professionelle Stellen zu wenden:\n"
                         "📞 <b>Krisentelefone:</b> (relevante Kontakte angeben)\n"
                         "🏥 <b>Professionelle Hilfe:</b> Wenn Sie sich Sorgen um Ihr emotionales Wohlbefinden machen, ziehen Sie eine Beratung durch einen Psychologen oder Therapeuten in Betracht.\n"
                         "👨‍👩‍👧‍👦 <b>Sprechen Sie mit Vertrauenspersonen:</b> Der Austausch mit Freunden oder Familie kann hilfreich sein.\n\n"
                         "✅ Die Teilnahme ist <b>völlig freiwillig</b>, und Sie können jederzeit durch Eingabe von <b>/stop</b> abbrechen.\n\n"
                         "🙏 Vielen Dank für Ihren Beitrag zur Wissenschaft!",

        'main_menu_message': 'Bitte wählen Sie eine Option:',
        'phq9_survey_button': "PHQ-9-Umfrage starten",
        'main_survey_button': "Hauptumfrage starten",


        'end_phq9_message': 'Vielen Dank für die Teilnahme an der Umfrage!',

        'answer_confirmation': 'Ihre Antwort wurde erfasst.',
        'age_validation_error': "Bitte geben Sie ein gültiges Alter ein (zwischen 18 und 100).",
        'age_numeric_error': "Bitte geben Sie für das Alter einen numerischen Wert ein.",

        'intro_phq9_message': '📝 In dieser Umfrage werden Ihnen eine Reihe von Fragen zu Ihrer Stimmung, Ihren Gedanken und Gefühlen gestellt. ',

        'question': 'Frage #',
        'starting_phq9': "<b>Wie oft fühlten Sie sich im Verlauf der <u>letzten 2 Wochen</u> durch die folgenden Beschwerden beeinträchtigt?</b>",
        'your_answer': 'Ihre Antwort: ',
        'checkmark': '✔️',

        "intro_main_message": "📝 In dieser Umfrage werden wir Ihnen eine Reihe von Fragen zu Ihren Gedanken, Gefühlen und Erfahrungen stellen. "
                                "Diese Fragen helfen uns, das emotionale Wohlbefinden und die täglichen Erfahrungen der Menschen besser zu verstehen.\n\n"
                                "💡 <b>Was Sie erwartet:</b>\n"
                                "✅ Sie beantworten <b>14 einfache Fragen</b> zu Ihren Emotionen, Ihrer Stimmung und Ihren Interaktionen mit anderen.\n"
                                "✅ Sie antworten auf Fragen, indem Sie <b>Sprachnachrichten aufnehmen</b>.\n"
                                "✅ Es gibt keine richtigen oder falschen Antworten – teilen Sie einfach, was für Sie wahr ist.\n"
                                "✅ Ihre Antworten sind <b>vertraulich</b> und werden nur für wissenschaftliche Forschungszwecke verwendet.\n\n"
                                "⚠️ <b>Wichtig:</b> Dieser Bot <b>bietet keine psychologische Hilfe</b>. Wenn Sie sich unwohl fühlen, können Sie jederzeit durch Eingabe von <b>/stop</b> abbrechen. "
                                "Wenn Sie Unterstützung benötigen, wenden Sie sich bitte an einen Fachmann.\n\n"
                                "👉 Wenn Sie bereit sind, legen wir los!",

        'end_main_survey_message': 'Vielen Dank für die Teilnahme an der Umfrage!',


        'voice_out_of_survey': 'Sie nehmen derzeit nicht an einer Umfrage teil. Bitte starten Sie die Hauptumfrage, um Fragen zu beantworten.',
        'voice_recieved': 'Ihre Sprachnachricht wurde empfangen. Wenn Sie eine weitere Antwort senden möchten, tun Sie dies bitte. Andernfalls können Sie mit der nächsten oder vorherigen Frage fortfahren.',
    },
    'ru': {
        'who_website': 'Дополнительная информация о депрессии',

        'help': 'Вот все доступные команды:\n'
                '/start - Начать бота\n'
                '/language - Изменить язык\n'
                '/help - Получить помощь\n',

        'yes': 'Да',
        'no': 'Нет',
        'no_answer': 'Без ответа',
        'in_past': 'В прошлом',
        'currently': 'В настоящее время',

        'previous': 'Назад',
        'next': 'Далее',
        'finish_button': 'Завершить опрос',

        'consent_message': 'Все собранные данные будут анонимизированы и использованы исключительно в научных целях. Вы согласны участвовать в исследовании?',
        'consent_yes': 'Спасибо за ваше согласие!',
        'consent_no': 'Если вы не согласны, вы не можете участвовать в исследовании. Если вы передумаете, вы можете начать опрос заново /start.',

        'gender_selection': 'Пожалуйста, выберите ваш пол:',
        'gender_male': 'Мужской',
        'gender_female': 'Женский',

        'age_selection': 'Пожалуйста, выберите ваш возраст:',



        'depression_diagnosis': 'Было ли у вас когда-либо диагностировано депрессивное расстройство?',
        'depressive_feelings': 'Считаете ли Вы, что у Вас была/есть депрессия?',

        'treatment_selection': 'Принимаете ли Вы в настоящее время/прошлом лекарства от депрессии?',




        'welcome_message': "👋 Здравствуйте!\n\n"
                         "Этот бот является частью <b>научного исследования</b>, целью которого является сбор данных об эмоциональном состоянии людей.\n\n"
                         "⚠️ <b>Важно:</b> Этот бот <b>не оказывает психологической помощи и не заменяет консультацию специалиста.</b>\n\n"
                         "❗ Если в процессе взаимодействия вы почувствуете дискомфорт или вам потребуется поддержка, рекомендуем обратиться к профессионалам:\n"
                         "📞 <b>Телефоны доверия:</b> (укажите актуальные контакты)\n"
                         "🏥 <b>Профессиональная помощь:</b> Если у вас есть вопросы касательно вашего эмоционального состояния, обратитесь к психологу или психотерапевту.\n"
                         "👨‍👩‍👧‍👦 <b>Поговорите с близкими:</b> Обсуждение своих чувств с людьми, которым вы доверяете, может помочь.\n\n"
                         "✅ Ваше участие <b>полностью добровольное</b>, и вы можете прекратить его в любой момент, просто введя <b>/stop</b>.\n\n"
                         "🙏 Спасибо за ваш вклад в науку!",

        'main_menu_message': 'Пожалуйста, выберите опцию:',
        'main_survey_button': 'Начать основной опрос',
        'phq9_survey_button': "Начать опрос PHQ-9",


        'end_phq9_message': 'Спасибо за участие в опросе!',

        'answer_confirmation': 'Ваш ответ был записан.',

        'age_validation_error': "Пожалуйста, введите допустимый возраст (от 18 до 100 лет).",
        'age_numeric_error': "Пожалуйста, введите числовое значение для возраста.",

        'intro_phq9_message': '📝 В этом опросе вам будут заданы ряд вопросов о вашем настроении, мыслях и чувствах. ',

        'question': 'Вопрос #',
        'starting_phq9': "<b>Как часто за <u>последние 2 недели</u> Вас беспокоили следующие проблемы?</b>",

        'your_answer': 'Ваш ответ: ',
        'checkmark': '✔️',

        "intro_main_message": "📝 В этом опросе мы зададим вам ряд вопросов о ваших мыслях, чувствах и переживаниях. "
                                "Эти вопросы помогут нам лучше понять эмоциональное благополучие и то, как люди переживают свою повседневную жизнь.\n\n"
                                "💡 <b>Чего ожидать?</b>\n"
                                "✅ Вы ответите на <b>14 простых вопросов</b> о ваших эмоциях, настроении и взаимодействии с другими.\n"
                                "✅ Вы будете отвечать на вопросы, записывая <b>голосовые сообщения</b>.\n"
                                "✅ Нет правильных или неправильных ответов – просто делитесь тем, чем что вам кажется правильным.\n"
                                "✅ Ваши ответы <b>конфиденциальны</b> и используются только для научных исследований.\n\n"
                                "⚠️ <b>Важно:</b> Этот бот <b>не предоставляет психологической помощи</b>. Если вам не комфортно, вы можете остановиться в любой момент, набрав <b>/stop</b>. "
                                "Если вам нужна поддержка, обратитесь к профессионалу.\n\n"
                                "👉 Если вы готовы, начнем!",

        'end_main_survey_message': 'Спасибо за участие в опросе!',

        'voice_out_of_survey': "Вы в настоящее время не участвуете в опросе. Пожалуйста, начните основной опрос, чтобы ответить на вопросы.",
        'voice_recieved': 'Ваше голосовое сообщение получено. Если вы хотите отправить еще один ответ, пожалуйста, сделайте это. В противном случае вы можете перейти к следующему или предыдущему вопросу.',
    },
}