from datetime import datetime
from localization import translations
from utils.db import (
    upsert_user_profile,
    upsert_phq_answers,
    get_connection,
    init_db,
    delete_user_records,
    load_session,
    save_session,
)

init_db()


def get_translation(user_id, key):
    language = context.get_user_info_field(user_id, "language")
    return translations[key].get(language)

# Database helpers
def get_user_profile(user_id):
    text = get_translation(user_id, "profile_template")

    fields = {
        "user_id": user_id,
        "age": context.get_user_info_field(user_id, "age"),
        "gender": context.get_user_info_field(user_id, "gender"),
        "language": context.get_user_info_field(user_id, "language"),
        "consent": context.get_user_info_field(user_id, "consent"),
        "treatment": context.get_user_info_field(user_id, "treatment"),
        "depressive": context.get_user_info_field(user_id, "depressive"),
    }

    for key in ["gender", "consent", "treatment", "depressive"]:
        val = fields.get(key)
        if val:
            translated = get_translation(user_id, val)
            if translated:
                fields[key] = translated

    lines = []
    for line in text.split("\n"):
        if "{treatment}" in line and not fields.get("treatment"):
            continue
        if "{depressive}" in line and not fields.get("depressive"):
            continue
        lines.append(line)
    text = "\n".join(lines)

    for key, value in fields.items():
        text = text.replace(f"{{{key}}}", str(value) if value is not None else "-")

    return text


class UserContext:
    """Manage user data with persistent storage in the database."""

    def __init__(self):
        # store ephemeral session data only
        self._session = {}

    def _ensure_session(self, user_id):
        if user_id not in self._session:
            data = load_session(user_id) or {}
            session = {
                "current_question_index": data.get("current_question_index", 0),
                "vm_ids": data.get("vm_ids", {}),
                "message_to_del": data.get("message_to_del"),
                "survey_message_id": data.get("survey_message_id"),
                "survey_controls_id": data.get("survey_controls_id"),
            }
            for i in range(8):
                session[f"phq_{i}"] = data.get(f"phq_{i}")
            self._session[user_id] = session

    def add_new_user(self, user_id):
        params = {
            "user_id": user_id,
            "consent": None,
            "gender": None,
            "age": None,
            "language": None,
            "treatment": None,
            "depressive": None,
            "first_name": None,
            "family_name": None,
            "username": None,
            "latitude": None,
            "longitude": None,
            "first_launch": datetime.utcnow().isoformat(timespec="seconds"),
        }

        upsert_user_profile(params)

        # prepare ephemeral fields
        self._session[user_id] = {
            "current_question_index": 0,
            "vm_ids": {},
            "message_to_del": None,
            "survey_message_id": None,
            "survey_controls_id": None,
        }
        save_session(user_id, self._session[user_id])

    def delete_user(self, user_id):
        self._session.pop(user_id, None)
        delete_user_records(user_id)

    def load_user_context(self):
        """Placeholder for backward compatibility."""
        pass

    def _load_profile(self, user_id):
        conn = get_connection()
        cur = conn.execute("SELECT * FROM user_profile WHERE user_id=?", (user_id,))
        row = cur.fetchone()
        return dict(row) if row else None

    def get_user_info(self, user_id):
        profile = self._load_profile(user_id)
        if profile is None:
            return None
        self._ensure_session(user_id)
        profile.update(self._session[user_id])
        return profile

    def get_user_info_field(self, user_id, field):
        if field in {"current_question_index", "vm_ids", "message_to_del", "survey_message_id", "survey_controls_id"}:
            self._ensure_session(user_id)
            return self._session[user_id].get(field)

        profile = self._load_profile(user_id)
        if profile is None:
            return None
        value = profile.get(field)
        if field in {"user_id", "age"} and value is not None:
            try:
                return int(value)
            except (TypeError, ValueError):
                return None
        return value

    def set_user_info_field(self, user_id, field, value):
        if field in {"current_question_index", "vm_ids", "message_to_del", "survey_message_id", "survey_controls_id"} or field.startswith("phq_"):
            self._ensure_session(user_id)
            self._session[user_id][field] = value
            save_session(user_id, self._session[user_id])
            return

        conn = get_connection()
        conn.execute(f"UPDATE user_profile SET {field}=? WHERE user_id=?", (value, user_id))
        conn.commit()

    def save_user_info(self, user_id):
        profile = self._load_profile(user_id)
        if profile is not None:
            upsert_user_profile(profile)

    def save_session(self, user_id):
        self._ensure_session(user_id)
        save_session(user_id, self._session[user_id])

    def save_phq_info(self, user_id):
        from survey import phq9_survey

        self._ensure_session(user_id)
        answers = {}
        for i in range(len(phq9_survey['en'])):
            answers[f"phq_{i}"] = self._session[user_id].get(f"phq_{i}")
        upsert_phq_answers(user_id, answers)

context = UserContext()
context.load_user_context()
