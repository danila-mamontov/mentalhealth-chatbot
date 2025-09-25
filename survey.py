from itertools import islice
from pathlib import Path
from utils.yaml_loader import load_simple_yaml
from utils.storage import context, get_translation


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


def _phq9_standard_options(language: str) -> list[str]:
    # All PHQ-9 questions share the same set of 4 options; take them from the first entry.
    first_q = next(iter(phq9_survey[language].keys()))
    return list(phq9_survey[language][first_q])


def get_phq9_total_questions(user_id=None, language=None) -> int:
    """Return total number of PHQ-9 screens including attention-check if configured."""
    if language is None and user_id is not None:
        language = context.get_user_info_field(user_id, "language")
    if language is None:
        language = "en"
    base = len(phq9_survey[language])
    attn_idx = context.get_user_info_field(user_id, "phq_attention_index") if user_id is not None else None
    return base + 1 if attn_idx is not None else base


def get_phq9_question_and_options(question_id, user_id=None, language=None):
    if language is None:
        language = context.get_user_info_field(user_id, "language")
    # Attention-check support: if the display index matches the configured attention index,
    # return the special instruction question with the same 4-option layout.
    attn_idx = context.get_user_info_field(user_id, "phq_attention_index") if user_id is not None else None
    if attn_idx is not None and question_id == attn_idx:
        # Expected option index (0-based); default to 1 -> "2"
        expected = context.get_user_info_field(user_id, "phq_attention_expected") or 1
        template = get_translation(user_id, "attention_check_instruction_msg") or "Attention check: Please select option {n} for this question."

        options = _phq9_standard_options(language)
        instruction = template.replace("{n}", f'"{options[expected]}"')
        return instruction, options

    # Map display index to real PHQ-9 item index when attention-check is present before it.
    real_index = question_id
    if attn_idx is not None and question_id > attn_idx:
        real_index = question_id - 1
    return next(islice(phq9_survey[language].items(), real_index, None))


def get_phq9_question_from_id(question_id):
    return next(islice(phq9_survey["en"].keys(), question_id, None))
