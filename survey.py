from itertools import islice
from pathlib import Path
from utils.yaml_loader import load_simple_yaml
from utils.storage import context


def _load_survey(name: str):
    surveys = {}
    base = Path(__file__).with_name('surveys') / name
    for file in base.glob('*.yml'):
        lang = file.stem
        surveys[lang] = load_simple_yaml(str(file))
    return surveys

phq9_survey = _load_survey('phq9')
main_survey = _load_survey('main')

emoji_mapping = {
    1: "\u25C6",  # 🟢 Green - Not at all
    2: "\u25C6",  # 🟡 Yellow - Several days
    3: "\u25C6",  # 🟠 Orange - More than half the days
    4: "\u25C6"   # 🔴 Red - Nearly every day
}

keycap_numbers = ["0️⃣","1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
marks = "✔️","⬅️","➡️"


def get_main_question(question_id, user_id=None, language=None):
    if language is None:
        language = context.get_user_info_field(user_id, "language")
    return next(islice(main_survey[language].keys(), question_id, None))


def get_phq9_question_and_options(question_id, user_id=None, language=None):
    if language is None:
        language = context.get_user_info_field(user_id, "language")
    return next(islice(phq9_survey[language].items(), question_id, None))


def get_phq9_question_from_id(question_id):
    return next(islice(phq9_survey["en"].keys(), question_id, None))
