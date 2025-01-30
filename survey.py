#https://www.pfizer.com/news/press-release/press-release-detail/pfizer_to_offer_free_public_access_to_mental_health_assessment_tools_to_improve_diagnosis_and_patient_care
phq9_survey = {
    'en': {
        "1. <b>Little interest or pleasure in doing things</b>": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        "2. <b>Feeling down, depressed, or hopeless</b>": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        "3. <b>Trouble falling asleep, staying asleep, or sleeping too much</b>": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        "4. <b>Feeling tired or having little energy</b>": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        "5. <b>Poor appetite or overeating</b>": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        "6. <b>Feeling bad about yourself - or that you’re a failure or have let yourself or your family down</b>": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        "7. <b>Trouble concentrating on things, such as reading the newspaper or watching television</b>": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        "8. <b>Moving or speaking so slowly that other people could have noticed. Or, the opposite - being so fidgety or restless that you have been moving around a lot more than usual</b>": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        "9. <b>Thoughts that you would be better off dead or of hurting yourself in some way</b>": ["Not at all", "Several days", "More than half the days", "Nearly every day"]
    },
    'de': {
        "1. <b>Wenig Interesse oder Freude an Ihren Tätigkeiten</b>": ["Überhaupt nicht", "An einzelnen Tagen", "An mehr als der Hälfte der Tage", "Beinahe jeden Tag"],
        "2. <b>Niedergeschlagenheit, Schwermut oder Hoffnungslosigkeit</b>": ["Überhaupt nicht", "An einzelnen Tagen", "An mehr als der Hälfte der Tage", "Beinahe jeden Tag"],
        "3. <b>Schwierigkeiten, ein- oder durchzuschlafen,oder vermehrter Schlaf</b>": ["Überhaupt nicht", "An einzelnen Tagen", "An mehr als der Hälfte der Tage", "Beinahe jeden Tag"],
        "4. <b>Müdigkeit oder Gefühl, keine Energie zu haben</b>": ["Überhaupt nicht", "An einzelnen Tagen", "An mehr als der Hälfte der Tage", "Beinahe jeden Tag"],
        "5. <b>Verminderter Appetit oder übermäßiges Bedürfnis zu essen</b>": ["Überhaupt nicht", "An einzelnen Tagen", "An mehr als der Hälfte der Tage", "Beinahe jeden Tag"],
        "6. <b>Schlechte Meinung von sich selbst; Gefühl, ein Versager zu sein oder die Familie enttäuscht zu haben</b>": ["Überhaupt nicht", "An einzelnen Tagen", "An mehr als der Hälfte der Tage", "Beinahe jeden Tag"],
        "7. <b>Schwierigkeiten, sich auf etwas zu konzentrieren, z. B. beim Zeitungslesen oder Fernsehen</b>": ["Überhaupt nicht", "An einzelnen Tagen", "An mehr als der Hälfte der Tage", "Beinahe jeden Tag"],
        "8. <b>Waren Ihre Bewegungen oder Ihre Sprache so verlangsamt, dass es auch anderen auffallen würde? Oder waren Sie im Gegenteil „zappelig“ oder ruhelos und hatten dadurch einen stärkeren Bewegungsdrang als sonst?</b>": ["Überhaupt nicht", "An einzelnen Tagen", "An mehr als der Hälfte der Tage", "Beinahe jeden Tag"],
        "9. <b>Gedanken, dass Sie lieber tot wären oder sich Leid zufügen möchten</b>": ["Überhaupt nicht", "An einzelnen Tagen", "An mehr als der Hälfte der Tage", "Beinahe jeden Tag"]
    },
    'ru': {
        "1. <b>Вам не хотелось ничего делать</b>": ["Ни разу", "Несколько дней", "Более недели", "Почти каждый день"],
        "2. <b>У Вас было плохое настроение, Вы были подавлены или испытывали чувство безысходности</b>": ["Ни разу", "Несколько дней", "Более недели", "Почти каждый день"],
        "3. <b>Вам было трудно заснуть, у Вас был прерывистый сон, или Вы слишком много спали</b>": ["Ни разу", "Несколько дней", "Более недели", "Почти каждый день"],
        "4. <b>Вы были утомлены, или у Вас было мало сил</b>": ["Ни разу", "Несколько дней", "Более недели", "Почти каждый день"],
        "5. <b>У Вас был плохой аппетит, или Вы переедали</b>": ["Ни разу", "Несколько дней", "Более недели", "Почти каждый день"],
        "6. <b>Вы плохо о себе думали: считали себя неудачником (неудачницей), или были в себе разочарованы, или считали, что подвели свою семью</b>": ["Ни разу", "Несколько дней", "Более недели", "Почти каждый день"],
        "7. <b>Вам было трудно сосредоточиться (например, на чтении газеты или на просмотре телепередач)</b>": ["Ни разу", "Несколько дней", "Более недели", "Почти каждый день"],
        "8. <b>Вы двигались или говорили настолько медленно, что окружающие это замечали? Или, наоборот, Вы были настолько суетливы или взбудоражены, что двигались гораздо больше обычного</b>": ["Ни разу", "Несколько дней", "Более недели", "Почти каждый день"],
        "9. <b>Вас посещали мысли о том, что Вам лучше было бы умереть, или о том, чтобы причинить себе какой-нибудь вред</b>": ["Ни разу", "Несколько дней", "Более недели", "Почти каждый день"]
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
        "1. How have you been feeling lately? Is there anything that has been bothering you or anything that has made you happy?": None,
        "2. What have been some good moments for you in the past few days? Were there any moments when you didn't feel so good?": None,
        "3. How do you spend your time? Is there anything new you've tried or something that helps you feel better?": None,
        "4. Do you feel like you're able to rest and recharge? How do you usually relax?": None,
        "5. How do you manage your daily tasks and commitments? Is there anything you'd like to spend more time on or focus on more?": None,
        "6. What are some moments in your life right now that bring you peace or satisfaction? Is there anything that's worrying you or needs your attention?": None,
        "7. How do you feel about interacting with others? Has anything brought you joy, or has something made you anxious or upset?": None,
        "8. How do you usually start your day? Is there anything that helps you get into a good mood, or would you like to change something in your morning routine?": None,
        "9. How do you deal with difficult situations? Has anything helped you, or not helped you, in recent days?": None,
        "10. How do you feel physically? Are there times when you feel especially energized or, on the contrary, tired?": None,
        "11. What helps you maintain a good mood? And if your mood drops, what do you do to bring it back up?": None,
        "12. How do you feel about your downtime and hobbies? Is there anything you'd like to do more of, or something you keep putting off?": None,
        "13. What has been the most important or meaningful thing for you in the past few weeks? It could be something small or something that affected you deeply.": None,
        "14. How would you rate your current life situation? What brings you joy, and what would you like to change if you had the chance?": None,
        "15. How do you feel overall — is there anything you'd like to improve, or is there something that brings you satisfaction and joy?": None
    },
    'de': {
        "1. Wie hast du dich in letzter Zeit gefühlt? Gibt es etwas, das dich belastet hat oder etwas, das dich glücklich gemacht hat?": None,
        "2. Was waren einige gute Momente für dich in den letzten Tagen? Gab es Momente, in denen du dich nicht so gut gefühlt hast?": None,
        "3. Wie verbringst du deine Zeit? Hast du etwas Neues ausprobiert oder etwas, das dir hilft, dich besser zu fühlen?": None,
        "4. Hast du das Gefühl, dass du dich ausruhen und neue Energie tanken kannst? Wie entspannst du dich normalerweise?": None,
        "5. Wie gehst du mit deinen täglichen Aufgaben und Verpflichtungen um? Gibt es etwas, worauf du mehr Zeit verwenden oder mehr Fokus legen möchtest?": None,
        "6. Welche Momente in deinem Leben bringen dir im Moment Frieden oder Zufriedenheit? Gibt es etwas, das dich beunruhigt oder Aufmerksamkeit erfordert?": None,
        "7. Wie fühlst du dich im Umgang mit anderen? Hat dich etwas erfreut oder gab es etwas, das dich ängstlich oder aufgeregt gemacht hat?": None,
        "8. Wie beginnst du normalerweise deinen Tag? Gibt es etwas, das dir hilft, in eine gute Stimmung zu kommen, oder würdest du etwas in deiner Morgenroutine ändern wollen?": None,
        "9. Wie gehst du mit schwierigen Situationen um? Hat dir etwas geholfen oder nicht geholfen in den letzten Tagen?": None,
        "10. Wie fühlst du dich körperlich? Gibt es Momente, in denen du dich besonders energiegeladen oder im Gegenteil müde fühlst?": None,
        "11. Was hilft dir, gute Laune zu behalten? Und wenn deine Laune sinkt, was tust du, um sie wieder zu heben?": None,
        "12. Wie stehst du zu deiner Freizeit und deinen Hobbys? Gibt es etwas, das du mehr tun möchtest oder etwas, das du immer wieder aufschiebst?": None,
        "13. Was war das Wichtigste oder Bedeutendste für dich in den letzten Wochen? Es könnte etwas Kleines oder etwas sein, das dich tief berührt hat.": None,
        "14. Wie würdest du deine aktuelle Lebenssituation bewerten? Was macht dich glücklich und was würdest du ändern, wenn du die Möglichkeit hättest?": None,
        "15. Wie fühlst du dich insgesamt — gibt es etwas, das du verbessern möchtest, oder gibt es etwas, das dir Zufriedenheit und Freude bringt?": None
    },
    'ru': {
        "1. Как ты себя чувствуешь в последнее время? Есть ли что-то, что тебя беспокоит или что-то, что тебя радует?": None,
        "2. Что было для тебя хорошего за последние несколько дней? Были ли моменты, когда ты не чувствовал себя так хорошо?": None,
        "3. Как ты проводишь свое время? Есть ли что-то новое, что ты попробовал или что помогает тебе чувствовать себя лучше?": None,
        "4. Чувствуешь ли ты, что тебе удается отдыхать и восстанавливать силы? Как ты обычно расслабляешься?": None,
        "5. Как ты справляешься с повседневными задачами и обязательствами? На что тебе хотелось бы уделять больше времени или внимания?": None,
        "6. Какие моменты в твоей жизни сейчас вызывают чувство удовлетворения или спокойствия? Есть ли что-то, что тебя беспокоит или требует внимания?": None,
        "7. Как ты относишься к общению с другими людьми? Было ли что-то, что принесло радость, или что-то, что заставило переживать?": None,
        "8. Как ты обычно начинаешь свой день? Есть ли что-то, что помогает тебе настроиться на хороший день или что бы ты хотел изменить в своей утренней рутине?": None,
        "9. Как ты справляешься с трудными ситуациями? Есть ли что-то, что тебе помогло или, наоборот, не помогло в последние дни?": None,
        "10. Как ты себя ощущаешь физически? Бывают ли моменты, когда ты чувствуешь себя особенно энергично или наоборот, устал?": None,
        "11. Что помогает тебе поддерживать хорошее настроение? И если твое настроение падает, что ты делаешь, чтобы вернуть его?": None,
        "12. Как ты относишься к своему времени для отдыха и хобби? Есть ли что-то, что тебе хотелось бы делать больше, или что ты откладываешь на потом?": None,
        "13. Что было самым важным или значимым для тебя в последние несколько недель? Это может быть что-то небольшое или что-то, что повлияло на тебя глубже.": None,
        "14. Как ты оцениваешь свою текущую жизненную ситуацию? Что тебя радует, а что бы ты хотел изменить, если бы была такая возможность?": None,
        "15. Как ты себя ощущаешь в целом — есть ли что-то, что тебе хотелось бы улучшить или, наоборот, что приносит удовлетворение и радость?": None
    }
}

