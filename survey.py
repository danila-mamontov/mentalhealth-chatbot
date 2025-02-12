from itertools import islice
from utils.storage import context

#https://www.pfizer.com/news/press-release/press-release-detail/pfizer_to_offer_free_public_access_to_mental_health_assessment_tools_to_improve_diagnosis_and_patient_care
phq9_survey = {
    'en': {
        "Little interest or pleasure in doing things": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        "Feeling down, depressed, or hopeless": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        "Trouble falling asleep, staying asleep, or sleeping too much": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        "Feeling tired or having little energy": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        "Poor appetite or overeating": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        "Feeling bad about yourself - or that you’re a failure or have let yourself or your family down": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        "Trouble concentrating on things, such as reading the newspaper or watching television": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        "Moving or speaking so slowly that other people could have noticed. Or, the opposite - being so fidgety or restless that you have been moving around a lot more than usual": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        "Thoughts that you would be better off dead or of hurting yourself in some way": ["Not at all", "Several days", "More than half the days", "Nearly every day"]
    },
    'de': {
        "Wenig Interesse oder Freude an Ihren Tätigkeiten": ["Überhaupt nicht", "An einzelnen Tagen", "An mehr als der Hälfte der Tage", "Beinahe jeden Tag"],
        "Niedergeschlagenheit, Schwermut oder Hoffnungslosigkeit": ["Überhaupt nicht", "An einzelnen Tagen", "An mehr als der Hälfte der Tage", "Beinahe jeden Tag"],
        "Schwierigkeiten, ein- oder durchzuschlafen,oder vermehrter Schlaf": ["Überhaupt nicht", "An einzelnen Tagen", "An mehr als der Hälfte der Tage", "Beinahe jeden Tag"],
        "Müdigkeit oder Gefühl, keine Energie zu haben": ["Überhaupt nicht", "An einzelnen Tagen", "An mehr als der Hälfte der Tage", "Beinahe jeden Tag"],
        "Verminderter Appetit oder übermäßiges Bedürfnis zu essen": ["Überhaupt nicht", "An einzelnen Tagen", "An mehr als der Hälfte der Tage", "Beinahe jeden Tag"],
        "Schlechte Meinung von sich selbst; Gefühl, ein Versager zu sein oder die Familie enttäuscht zu haben": ["Überhaupt nicht", "An einzelnen Tagen", "An mehr als der Hälfte der Tage", "Beinahe jeden Tag"],
        "Schwierigkeiten, sich auf etwas zu konzentrieren, z. B. beim Zeitungslesen oder Fernsehen": ["Überhaupt nicht", "An einzelnen Tagen", "An mehr als der Hälfte der Tage", "Beinahe jeden Tag"],
        "Waren Ihre Bewegungen oder Ihre Sprache so verlangsamt, dass es auch anderen auffallen würde? Oder waren Sie im Gegenteil „zappelig“ oder ruhelos und hatten dadurch einen stärkeren Bewegungsdrang als sonst?": ["Überhaupt nicht", "An einzelnen Tagen", "An mehr als der Hälfte der Tage", "Beinahe jeden Tag"],
        "Gedanken, dass Sie lieber tot wären oder sich Leid zufügen möchten": ["Überhaupt nicht", "An einzelnen Tagen", "An mehr als der Hälfte der Tage", "Beinahe jeden Tag"]
    },
    'ru': {
        "Вам не хотелось ничего делать": ["Ни разу", "Несколько дней", "Более недели", "Почти каждый день"],
        "У Вас было плохое настроение, Вы были подавлены или испытывали чувство безысходности": ["Ни разу", "Несколько дней", "Более недели", "Почти каждый день"],
        "Вам было трудно заснуть, у Вас был прерывистый сон, или Вы слишком много спали": ["Ни разу", "Несколько дней", "Более недели", "Почти каждый день"],
        "Вы были утомлены, или у Вас было мало сил": ["Ни разу", "Несколько дней", "Более недели", "Почти каждый день"],
        "У Вас был плохой аппетит, или Вы переедали": ["Ни разу", "Несколько дней", "Более недели", "Почти каждый день"],
        "Вы плохо о себе думали: считали себя неудачником (неудачницей), или были в себе разочарованы, или считали, что подвели свою семью": ["Ни разу", "Несколько дней", "Более недели", "Почти каждый день"],
        "Вам было трудно сосредоточиться (например, на чтении газеты или на просмотре телепередач)": ["Ни разу", "Несколько дней", "Более недели", "Почти каждый день"],
        "Вы двигались или говорили настолько медленно, что окружающие это замечали? Или, наоборот, Вы были настолько суетливы или взбудоражены, что двигались гораздо больше обычного": ["Ни разу", "Несколько дней", "Более недели", "Почти каждый день"],
        "Вас посещали мысли о том, что Вам лучше было бы умереть, или о том, чтобы причинить себе какой-нибудь вред": ["Ни разу", "Несколько дней", "Более недели", "Почти каждый день"]
    }
}

emoji_mapping = {
    1: "\u25C6",  # 🟢 Green - Not at all
    2: "\u25C6",  # 🟡 Yellow - Several days
    3: "\u25C6",  # 🟠 Orange - More than half the days
    4: "\u25C6"   # 🔴 Red - Nearly every day
}

keycap_numbers = ["0️⃣","1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
marks = "✔️","⬅️","➡️"

WBMMS_survey = {
    'en': {
        "I've been feeling optimistic about the future. \n💭 Do you generally feel hopeful and positive about what lies ahead, including your personal life, work, and relationships?": None,
        "I've been feeling useful. \n🔧 Do you feel that your contributions, whether at work, home, or in social settings, are valued and meaningful?": None,
        "I've been feeling relaxed. \n🧘‍♂️ Have you been able to stay calm and free from excessive stress or tension in your daily life?": None,
        "I've been feeling interested in other people. \n🗣️ Do you enjoy engaging with others, showing curiosity about their thoughts, feelings, and experiences?": None,
        "I've had energy to spare. \n⚡ Do you feel physically and mentally energized throughout the day, with enough motivation to complete tasks and engage in activities?": None,
        "I've been dealing with problems well. \n🛠️ How confident are you in your ability to handle difficulties, solve challenges, and stay resilient in stressful situations?": None,
        "I've been thinking clearly. \n🧠 Have you been able to focus, organize your thoughts, and make decisions without excessive confusion or mental fog?": None,
        "I've been feeling good about myself. \n😊 Do you have a positive self-image and feel comfortable with who you are, without excessive self-doubt or criticism?": None,
        "I've been feeling close to other people. \n❤️ Do you experience a sense of emotional connection and belonging with friends, family, or other people in your life?": None,
        "I've been feeling confident. \n💪 Have you felt self-assured in your abilities, decisions, and overall sense of self-worth?": None,
        "I've been able to make up my own mind about things. \n🤔 Do you find it easy to make decisions on your own without needing advice or assistance from others?": None,
        "I've been feeling loved. \n💖 Have you felt appreciated, supported, and cared for by the people around you?": None,
        "I've been interested in new things. \n🌍 Are you curious and open to exploring new ideas, hobbies, or experiences?": None,
        "I've been feeling cheerful. \n😃 Have you generally felt happy, in a good mood, and able to find enjoyment in daily life?": None
    },
    'de': {
        "Ich war optimistisch in Bezug auf die Zukunft. \n💭 Fühlen Sie sich im Allgemeinen hoffnungsvoll und positiv in Bezug auf Ihre persönliche Zukunft, Arbeit und Beziehungen?": None,
        "Ich habe mich nützlich gefühlt. \n🔧 Haben Sie das Gefühl, dass Ihre Beiträge in Arbeit, Familie oder sozialem Umfeld geschätzt werden und einen Wert haben?": None,
        "Ich habe mich entspannt gefühlt. \n🧘‍♂️ Konnten Sie in Ihrem Alltag ruhig bleiben und sich von übermäßigem Stress oder Anspannung fernhalten?": None,
        "Ich habe mich für andere Menschen interessiert. \n🗣️ Genießen Sie es, mit anderen Menschen zu interagieren, sich für ihre Gedanken, Gefühle und Erfahrungen zu interessieren?": None,
        "Ich hatte Energie übrig. \n⚡ Fühlen Sie sich körperlich und geistig energiegeladen, mit genug Motivation für alltägliche Aufgaben und Aktivitäten?": None,
        "Ich bin gut mit Problemen umgegangen. \n🛠️ Wie sicher sind Sie, dass Sie Herausforderungen bewältigen und in stressigen Situationen widerstandsfähig bleiben können?": None,
        "Ich habe klar gedacht. \n🧠 Konnten Sie sich konzentrieren, Ihre Gedanken ordnen und Entscheidungen ohne große Verwirrung oder geistige Unklarheit treffen?": None,
        "Ich habe mich gut gefühlt. \n😊 Haben Sie ein positives Selbstbild und fühlen sich wohl mit sich selbst, ohne übermäßige Selbstzweifel oder Kritik?": None,
        "Ich habe mich anderen Menschen nahe gefühlt. \n❤️ Erleben Sie emotionale Verbundenheit und ein Zugehörigkeitsgefühl mit Freunden, Familie oder anderen Menschen?": None,
        "Ich habe mich selbstbewusst gefühlt. \n💪 Fühlen Sie sich selbstsicher in Bezug auf Ihre Fähigkeiten, Entscheidungen und Ihr allgemeines Selbstwertgefühl?": None,
        "Ich konnte mir meine eigene Meinung über Dinge bilden. \n🤔 Fällt es Ihnen leicht, Entscheidungen selbstständig zu treffen, ohne dabei auf die Hilfe oder Beratung anderer angewiesen zu sein?": None,
        "Ich habe mich geliebt gefühlt. \n💖 Haben Sie sich von den Menschen um Sie herum geschätzt, unterstützt und geliebt gefühlt?": None,
        "Ich war an neuen Dingen interessiert. \n🌍 Sind Sie neugierig und offen für neue Ideen, Hobbys oder Erfahrungen?": None,
        "Ich habe mich fröhlich gefühlt. \n😃 Haben Sie sich in letzter Zeit oft glücklich, in guter Stimmung und mit Freude am Leben gefühlt?": None
    },
    'ru': {
        "Я чувствовал(а) себя оптимистично в отношении будущего. \n💭 Чувствуете ли Вы надежду и позитив в отношении своего будущего, включая личную жизнь, работу и отношения?": None,
        "Я чувствовал(а) себя полезным(ой). \n🔧 Ощущаете ли Вы, что Ваши действия и вклад в работу, семью или общество значимы и ценны?": None,
        "Я чувствовал(а) себя расслабленно. \n🧘‍♂️ Удавалось ли Вам сохранять спокойствие и избегать чрезмерного стресса или напряжения в повседневной жизни?": None,
        "Мне было интересно общаться с другими людьми. \n🗣️ Испытываете ли Вы интерес к окружающим, их мыслям, чувствам и переживаниям? Нравится ли Вам взаимодействовать с ними?": None,
        "У меня было достаточно энергии. \n⚡ Чувствуете ли Вы бодрость и мотивацию для выполнения повседневных задач и участия в различных активностях?": None,
        "Я хорошо справлялся(ась) с проблемами. \n🛠️ Насколько уверенно Вы решаете жизненные трудности и сохраняете устойчивость в сложных ситуациях?": None,
        "Я мыслил(а) ясно. \n🧠 Легко ли Вам сосредотачиваться, анализировать информацию и принимать решения без путаницы в мыслях?": None,
        "Я чувствовал(а) себя хорошо. \n😊 Чувствуете ли Вы уверенность в себе и в своих способностях, без чрезмерного самокритицизма?": None,
        "Я чувствовал(а) себя близким(ой) к другим людям. \n❤️ Испытываете ли Вы эмоциональную связь и ощущение принадлежности с семьей, друзьями или коллегами?": None,
        "Я чувствовал(а) себя уверенно. \n💪 Насколько Вы уверены в себе, своих решениях и своих возможностях?": None,
        "Я мог(ла) самостоятельно принимать решения. \n🤔 Легко ли Вам принимать решения без необходимости обращаться за помощью или советом к другим людям?": None,
        "Я чувствовал(а) себя любимым(ой). \n💖 Чувствуете ли Вы поддержку, заботу и любовь со стороны близких людей?": None,
        "Мне было интересно узнавать что-то новое. \n🌍 Открыты ли Вы к новым знаниям, впечатлениям и опыту?": None,
        "Я чувствовал(а) себя жизнерадостно. \n😃 Часто ли Вы испытываете радость, счастье и позитивный настрой в жизни?": None
    }
}

def get_wbmms_question(question_id, user_id=None, language=None):
    if language is None:
        language = context.get_user_info_field(user_id, "language")
    else:
        language = language
    return next(islice(WBMMS_survey[language].keys(), question_id, None))

def get_phq9_question_and_options(question_id, user_id=None, language=None):
    if language is None:
        language = context.get_user_info_field(user_id, "language")
    else:
        language = language
    return next(islice(phq9_survey[language].items(), question_id, None))

def get_phq9_question_from_id(question_id):
    return next(islice(phq9_survey["en"].keys(), question_id, None))
