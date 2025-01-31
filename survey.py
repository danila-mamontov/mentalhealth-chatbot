#https://www.pfizer.com/news/press-release/press-release-detail/pfizer_to_offer_free_public_access_to_mental_health_assessment_tools_to_improve_diagnosis_and_patient_care
phq9_survey = {
    'en': {
        "<i><b>Little interest or pleasure in doing things</b></i>": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        "<i><b>Feeling down, depressed, or hopeless</b></i>": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        "<i><b>Trouble falling asleep, staying asleep, or sleeping too much</b></i>": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        "<i><b>Feeling tired or having little energy</b></i>": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        "<i><b>Poor appetite or overeating</b></i>": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        "<i><b>Feeling bad about yourself - or that you’re a failure or have let yourself or your family down</b></i>": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        "<i><b>Trouble concentrating on things, such as reading the newspaper or watching television</b></i>": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        "<i><b>Moving or speaking so slowly that other people could have noticed. Or, the opposite - being so fidgety or restless that you have been moving around a lot more than usual</b></i>": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        "<i><b>Thoughts that you would be better off dead or of hurting yourself in some way</b></i>": ["Not at all", "Several days", "More than half the days", "Nearly every day"]
    },
    'de': {
        "<i><b>Wenig Interesse oder Freude an Ihren Tätigkeiten</b></i>": ["Überhaupt nicht", "An einzelnen Tagen", "An mehr als der Hälfte der Tage", "Beinahe jeden Tag"],
        "<i><b>Niedergeschlagenheit, Schwermut oder Hoffnungslosigkeit</b></i>": ["Überhaupt nicht", "An einzelnen Tagen", "An mehr als der Hälfte der Tage", "Beinahe jeden Tag"],
        "<i><b>Schwierigkeiten, ein- oder durchzuschlafen,oder vermehrter Schlaf</b></i>": ["Überhaupt nicht", "An einzelnen Tagen", "An mehr als der Hälfte der Tage", "Beinahe jeden Tag"],
        "<i><b>Müdigkeit oder Gefühl, keine Energie zu haben</b></i>": ["Überhaupt nicht", "An einzelnen Tagen", "An mehr als der Hälfte der Tage", "Beinahe jeden Tag"],
        "<i><b>Verminderter Appetit oder übermäßiges Bedürfnis zu essen</b></i>": ["Überhaupt nicht", "An einzelnen Tagen", "An mehr als der Hälfte der Tage", "Beinahe jeden Tag"],
        "<i><b>Schlechte Meinung von sich selbst; Gefühl, ein Versager zu sein oder die Familie enttäuscht zu haben</b></i>": ["Überhaupt nicht", "An einzelnen Tagen", "An mehr als der Hälfte der Tage", "Beinahe jeden Tag"],
        "<i><b>Schwierigkeiten, sich auf etwas zu konzentrieren, z. B. beim Zeitungslesen oder Fernsehen</b></i>": ["Überhaupt nicht", "An einzelnen Tagen", "An mehr als der Hälfte der Tage", "Beinahe jeden Tag"],
        "<i><b>Waren Ihre Bewegungen oder Ihre Sprache so verlangsamt, dass es auch anderen auffallen würde? Oder waren Sie im Gegenteil „zappelig“ oder ruhelos und hatten dadurch einen stärkeren Bewegungsdrang als sonst?</b></i>": ["Überhaupt nicht", "An einzelnen Tagen", "An mehr als der Hälfte der Tage", "Beinahe jeden Tag"],
        "<i><b>Gedanken, dass Sie lieber tot wären oder sich Leid zufügen möchten</b></i>": ["Überhaupt nicht", "An einzelnen Tagen", "An mehr als der Hälfte der Tage", "Beinahe jeden Tag"]
    },
    'ru': {
        "<i><b>Вам не хотелось ничего делать</b></i>": ["Ни разу", "Несколько дней", "Более недели", "Почти каждый день"],
        "<i><b>У Вас было плохое настроение, Вы были подавлены или испытывали чувство безысходности</b></i>": ["Ни разу", "Несколько дней", "Более недели", "Почти каждый день"],
        "<i><b>Вам было трудно заснуть, у Вас был прерывистый сон, или Вы слишком много спали</b></i>": ["Ни разу", "Несколько дней", "Более недели", "Почти каждый день"],
        "<i><b>Вы были утомлены, или у Вас было мало сил</b></i>": ["Ни разу", "Несколько дней", "Более недели", "Почти каждый день"],
        "<i><b>У Вас был плохой аппетит, или Вы переедали</b></i>": ["Ни разу", "Несколько дней", "Более недели", "Почти каждый день"],
        "<i><b>Вы плохо о себе думали: считали себя неудачником (неудачницей), или были в себе разочарованы, или считали, что подвели свою семью</b></i>": ["Ни разу", "Несколько дней", "Более недели", "Почти каждый день"],
        "<i><b>Вам было трудно сосредоточиться (например, на чтении газеты или на просмотре телепередач)</b></i>": ["Ни разу", "Несколько дней", "Более недели", "Почти каждый день"],
        "<i><b>Вы двигались или говорили настолько медленно, что окружающие это замечали? Или, наоборот, Вы были настолько суетливы или взбудоражены, что двигались гораздо больше обычного</b></i>": ["Ни разу", "Несколько дней", "Более недели", "Почти каждый день"],
        "<i><b>Вас посещали мысли о том, что Вам лучше было бы умереть, или о том, чтобы причинить себе какой-нибудь вред</b></i>": ["Ни разу", "Несколько дней", "Более недели", "Почти каждый день"]
    }
}

emoji_mapping = {
    1: "\U0001F7E2",  # 🟢 Green - Not at all
    2: "\U0001F7E1",  # 🟡 Yellow - Several days
    3: "\U0001F7E0",  # 🟠 Orange - More than half the days
    4: "\U0001F534"   # 🔴 Red - Nearly every day
}

main_survey = {
    'en': {
        "How optimistic do you feel about your future, including your personal growth, career, relationships, and overall well-being?": None,
        "How useful and needed do you feel in your daily life, whether at work, in your family, or within your social circle?": None,
        "Do you generally feel relaxed and at ease, both physically and mentally, regardless of the challenges you may face?": None,
        "Are you genuinely interested in other people, including their thoughts, feelings, and experiences, and do you enjoy engaging with them?": None,
        "Do you feel energetic and full of strength, with enough motivation to accomplish your daily tasks and pursue your interests?": None,
        "How well do you manage and cope with challenges, difficulties, and unexpected situations in different areas of your life?": None,
        "How clearly and logically do you think, and do you find it easy to focus, make decisions, and solve problems effectively?": None,
        "Do you feel good about yourself, including your abilities, personality, and overall self-worth, without excessive self-doubt?": None,
        "How close and connected do you feel to other people, including family, friends, colleagues, or your community?": None,
        "Do you feel confident in yourself, your decisions, and your abilities, without being overly self-critical or hesitant?": None,
        "How easy is it for you to make your own decisions and form your own opinions without being overly influenced by others?": None,
        "Do you feel loved, valued, and supported by those around you, and do you experience meaningful emotional connections?": None,
        "Are you naturally curious and open to learning new things, trying new experiences, or exploring different perspectives?": None,
        "Do you often feel cheerful, happy, and in a positive mood, with an overall sense of contentment and enjoyment in life?": None
    },
    'de': {
        "Wie optimistisch fühlen Sie sich in Bezug auf Ihre Zukunft, einschließlich persönlichem Wachstum, Karriere, Beziehungen und allgemeinem Wohlbefinden?": None,
        "Wie nützlich und gebraucht fühlen Sie sich in Ihrem täglichen Leben, sei es bei der Arbeit, in der Familie oder in Ihrem sozialen Umfeld?": None,
        "Fühlen Sie sich im Allgemeinen entspannt und wohl, sowohl körperlich als auch geistig, unabhängig von den Herausforderungen, denen Sie begegnen?": None,
        "Sind Sie wirklich an anderen Menschen interessiert, einschließlich ihrer Gedanken, Gefühle und Erfahrungen, und genießen Sie den Austausch mit ihnen?": None,
        "Fühlen Sie sich energiegeladen und stark, mit genug Motivation, um Ihre täglichen Aufgaben zu erledigen und Ihre Interessen zu verfolgen?": None,
        "Wie gut bewältigen Sie Herausforderungen, Schwierigkeiten und unerwartete Situationen in verschiedenen Bereichen Ihres Lebens?": None,
        "Denken Sie klar und logisch? Fällt es Ihnen leicht, sich zu konzentrieren, Entscheidungen zu treffen und Probleme effektiv zu lösen?": None,
        "Fühlen Sie sich gut in Ihrer Haut, einschließlich Ihrer Fähigkeiten, Persönlichkeit und Ihres Selbstwertgefühls, ohne übermäßige Selbstzweifel?": None,
        "Wie nah und verbunden fühlen Sie sich mit anderen Menschen, einschließlich Familie, Freunden, Kollegen oder Ihrer Gemeinschaft?": None,
        "Fühlen Sie sich selbstbewusst in Bezug auf sich selbst, Ihre Entscheidungen und Ihre Fähigkeiten, ohne übermäßig selbstkritisch oder zögerlich zu sein?": None,
        "Wie einfach ist es für Sie, eigene Entscheidungen zu treffen und Ihre eigenen Meinungen zu formen, ohne zu stark von anderen beeinflusst zu werden?": None,
        "Fühlen Sie sich geliebt, wertgeschätzt und von den Menschen um Sie herum unterstützt? Erleben Sie bedeutungsvolle emotionale Verbindungen?": None,
        "Sind Sie von Natur aus neugierig und offen für das Lernen neuer Dinge, das Ausprobieren neuer Erfahrungen oder das Erkunden unterschiedlicher Perspektiven?": None,
        "Fühlen Sie sich oft fröhlich, glücklich und in einer positiven Stimmung, mit einem allgemeinen Gefühl der Zufriedenheit und Lebensfreude?": None
    },
    'ru': {
        "Насколько оптимистично Вы смотрите в будущее, включая личностный рост, карьеру, отношения и общее благополучие?": None,
        "Насколько полезным и нужным Вы себя ощущаете в повседневной жизни, будь то на работе, в семье или в социальном окружении?": None,
        "Чувствуете ли Вы себя расслабленно и комфортно, как физически, так и психологически, несмотря на возникающие трудности?": None,
        "Проявляете ли Вы искренний интерес к другим людям, их мыслям, чувствам и переживаниям? Нравится ли Вам общаться с ними?": None,
        "Чувствуете ли Вы прилив энергии и сил, с достаточной мотивацией для выполнения повседневных задач и достижения целей?": None,
        "Насколько хорошо Вы справляетесь с трудностями, вызовами и неожиданными ситуациями в различных сферах жизни?": None,
        "Насколько ясно и логично Вы мыслите? Легко ли Вам концентрироваться, принимать решения и эффективно решать проблемы?": None,
        "Чувствуете ли Вы себя хорошо в своей шкуре, включая свои способности, личность и уровень самооценки, без чрезмерных сомнений?": None,
        "Насколько близкими и значимыми для Вас являются отношения с окружающими людьми, включая семью, друзей, коллег или сообщество?": None,
        "Чувствуете ли Вы уверенность в себе, своих решениях и возможностях, без чрезмерной самокритики или неуверенности?": None,
        "Насколько легко Вам принимать собственные решения и формировать собственное мнение, не поддаваясь излишнему влиянию окружающих?": None,
        "Чувствуете ли Вы себя любимым, ценным и поддерживаемым окружающими людьми? Испытываете ли Вы значимые эмоциональные связи?": None,
        "Проявляете ли Вы естественное любопытство и открыты ли Вы для изучения нового, пробования новых вещей и различных точек зрения?": None,
        "Часто ли Вы испытываете радость, счастье и позитивный настрой, ощущая общее удовлетворение и удовольствие от жизни?": None
    }
}
