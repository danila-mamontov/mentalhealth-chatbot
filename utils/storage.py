from localization import translations
from utils.db import (
    upsert_user_profile,
    upsert_phq_answers,
    get_connection,
    init_db,
    delete_user_records,
    get_survey_progress,
    get_first_unanswered_question,
)

init_db()


def get_translation(t_id, key):
    language = context.get_user_info_field(t_id, "language")
    # Try exact key first
    entry = translations.get(key)
    val = entry.get(language) if entry else None
    if val:
        return val
    # Fallbacks: swap _msg <-> base and base_message
    candidates = []
    if key.endswith("_msg"):
        base = key[:-4]
        candidates = [base, f"{base}_message"]
    else:
        candidates = [f"{key}_msg", f"{key}_message"]
    for cand in candidates:
        e = translations.get(cand)
        if e:
            v = e.get(language)
            if v:
                return v
    # As last resort, return any available language value for the key
    for cand in [key] + candidates:
        e = translations.get(cand)
        if e:
            any_val = next(iter(e.values()), None)
            if any_val:
                return any_val
    return None

# Database helpers
def load_user_info(t_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM user_profile WHERE t_id=? ORDER BY id DESC LIMIT 1", (t_id,)
    ).fetchone()
    return dict(row) if row else None

def get_user_profile(t_id):
    text = get_translation(t_id, "profile_template_msg")

    fields = {
        "user_id": context.get_user_info_field(t_id, "id"),
        "age": context.get_user_info_field(t_id, "age"),
        "gender": context.get_user_info_field(t_id, "gender"),
        "language": context.get_user_info_field(t_id, "language"),
        "consent": context.get_user_info_field(t_id, "consent"),
        "treatment": context.get_user_info_field(t_id, "treatment"),
        "depressive": context.get_user_info_field(t_id, "depressive"),
    }

    for key in ["gender", "consent", "treatment", "depressive"]:
        val = fields.get(key)
        if val:
            translated = get_translation(t_id, f"{val}_msg")
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
        # store ephemeral session data only, keyed by internal id
        self._session = {}
        self._tid_to_id = {}
        self._active_uid = {}

    def _ensure_session(self, uid):
        self._session.setdefault(uid, {
            "current_question_index": 0,
            "vm_ids": {},
            "message_to_del": None,
            "survey_message_id": None,
            "survey_controls_id": None,
            "welcome_message_id": None,
            "reading_text_file_id": None,
            "reading_text_confirm_msg_id": None,
            "reading_text_voice_msg_id": None,
            "reading_text_total_duration": None,
        })

    def _set_active_uid(self, t_id, uid):
        self._active_uid[t_id] = uid
        self._tid_to_id[t_id] = uid

    def _resolve_latest_uid(self, t_id):
        row = get_connection().execute(
            "SELECT id FROM user_profile WHERE t_id=? ORDER BY id DESC LIMIT 1", (t_id,)
        ).fetchone()
        return row["id"] if row else None

    def add_new_user(self, t_id):
        params = {
            "id": None,
            "t_id": t_id,
            "consent": None,
            "gender": None,
            "age": None,
            "language": None,
            "treatment": None,
            "depressive": None,
        }

        upsert_user_profile(params)
        uid = self._resolve_latest_uid(t_id)
        if uid is None:
            return

        self._set_active_uid(t_id, uid)

        # prepare ephemeral fields
        if uid is not None:
            self._session[uid] = {
                "current_question_index": 0,
                "vm_ids": {},
                "message_to_del": None,
                "survey_message_id": None,
                "survey_controls_id": None,
                "welcome_message_id": None,
                "reading_text_file_id": None,
                "reading_text_confirm_msg_id": None,
                "reading_text_voice_msg_id": None,
                "reading_text_total_duration": None,
            }

    def delete_user(self, t_id):
        uid = self._get_id(t_id)
        if uid is not None:
            self._session.pop(uid, None)
            delete_user_records(uid)

    def load_user_context(self):
        """Placeholder for backward compatibility."""
        pass

    def _get_id(self, t_id):
        uid = self._active_uid.get(t_id) or self._tid_to_id.get(t_id)
        if uid is not None:
            return uid
        uid = self._resolve_latest_uid(t_id)
        if uid is not None:
            self._set_active_uid(t_id, uid)
        return uid

    def _load_profile_by_uid(self, uid):
        row = get_connection().execute("SELECT * FROM user_profile WHERE id=?", (uid,)).fetchone()
        return dict(row) if row else None

    def _load_profile(self, t_id):
        uid = self._get_id(t_id)
        if uid is None:
            return None
        return self._load_profile_by_uid(uid)

    def get_user_info(self, t_id):
        profile = self._load_profile(t_id)
        if profile is None:
            return None
        uid = profile["id"]
        self._ensure_session(uid)
        profile.update(self._session[uid])
        return profile

    def get_user_info_field(self, t_id, field):
        if field in {"current_question_index", "vm_ids", "message_to_del", "survey_message_id", "survey_controls_id", "welcome_message_id", "reading_text_file_id", "reading_text_confirm_msg_id", "reading_text_voice_msg_id", "reading_text_total_duration"} or field.startswith("phq_"):
            uid = self._get_id(t_id)
            if uid is None:
                return None
            self._ensure_session(uid)
            return self._session[uid].get(field)

        profile = self._load_profile(t_id)
        if profile is None:
            return None
        value = profile.get(field)
        if field in {"id", "age"} and value is not None:
            try:
                return int(value)
            except (TypeError, ValueError):
                return None
        return value

    def set_user_info_field(self, t_id, field, value):
        if field in {"current_question_index", "vm_ids", "message_to_del", "survey_message_id", "survey_controls_id", "welcome_message_id", "reading_text_file_id", "reading_text_confirm_msg_id", "reading_text_voice_msg_id", "reading_text_total_duration"} or field.startswith("phq_"):
            uid = self._get_id(t_id)
            if uid is None:
                return
            self._ensure_session(uid)
            self._session[uid][field] = value
            return

        uid = self._get_id(t_id)
        if uid is None:
            return
        conn = get_connection()
        conn.execute(f"UPDATE user_profile SET {field}=? WHERE id=?", (value, uid))
        conn.commit()

    def save_user_info(self, t_id):
        profile = self._load_profile(t_id)
        if profile is not None:
            upsert_user_profile(profile)

    def save_phq_info(self, t_id):
        from survey import phq9_survey

        uid = self._get_id(t_id)
        if uid is None:
            return
        self._ensure_session(uid)
        answers = {}
        for i in range(len(phq9_survey['en'])):
            answers[f"phq_{i}"] = self._session[uid].get(f"phq_{i}")
        # add attention check result
        answers["attention_failed"] = self._session[uid].get("phq_attention_failed", 0)
        upsert_phq_answers(uid, answers)

    def reenroll_user(self, t_id):
        """Create a fresh participant profile for the same Telegram id and make it active."""
        conn = get_connection()
        prev_uid = self._get_id(t_id)
        prev_lang = None
        if prev_uid is not None:
            prev = conn.execute("SELECT language FROM user_profile WHERE id=?", (prev_uid,)).fetchone()
            prev_lang = prev["language"] if prev else None

        params = {
            "id": None,
            "t_id": t_id,
            "consent": None,
            "gender": None,
            "age": None,
            "language": prev_lang,
            "treatment": None,
            "depressive": None,
        }
        upsert_user_profile(params)

        uid = self._resolve_latest_uid(t_id)
        if uid is None:
            return None
        self._set_active_uid(t_id, uid)
        self._session[uid] = {
            "current_question_index": 0,
            "vm_ids": {},
            "message_to_del": None,
            "survey_message_id": None,
            "survey_controls_id": None,
            "welcome_message_id": None,
            "reading_text_file_id": None,
            "reading_text_confirm_msg_id": None,
            "reading_text_voice_msg_id": None,
            "reading_text_total_duration": None,
        }
        return uid

context = UserContext()
context.load_user_context()

# Re-export get_survey_progress and get_first_unanswered_question from db module for convenience
__all__ = ['context', 'get_translation', 'get_user_profile', 'get_survey_progress', 'get_first_unanswered_question']
