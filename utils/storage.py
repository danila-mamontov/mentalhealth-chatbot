from localization import translations
from utils.db import (
    upsert_user_profile,
    upsert_phq_answers,
    get_connection,
    init_db,
    delete_user_records,
)

init_db()


def get_translation(user_id, key):
    language = context.get_user_info_field(user_id, "language")
    return translations[key].get(language)

# Database helpers
def load_user_info(user_id):
    conn = get_connection()
    cur = conn.execute("SELECT * FROM user_profile WHERE user_id=?", (user_id,))
    row = cur.fetchone()
    if row:
        return dict(row)
    return None

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

    for key, value in fields.items():
        text = text.replace(f"{{{key}}}", str(value) if value is not None else "-")

    return text


class UserContext:
    """Manage user data with persistent storage in the database."""

    def __init__(self):
        # store ephemeral session data only
        self._session = {}

    def _ensure_session(self, user_id):
        self._session.setdefault(user_id, {
            "current_question_index": 0,
            "vm_ids": {},
            "message_to_del": None,
            "survey_message_id": None,
            "survey_controls_id": None,
        })

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
            return

        conn = get_connection()
        conn.execute(f"UPDATE user_profile SET {field}=? WHERE user_id=?", (value, user_id))
        conn.commit()

    def save_user_info(self, user_id):
        profile = self._load_profile(user_id)
        if profile is not None:
            upsert_user_profile(profile)

    def save_phq_info(self, user_id):
        from survey import phq9_survey

        self._ensure_session(user_id)
        answers = {}
        for i in range(len(phq9_survey['en'])):
            answers[f"phq_{i}"] = self._session[user_id].get(f"phq_{i}")
        upsert_phq_answers(user_id, answers)

context = UserContext()
context.load_user_context()

#     user_context = ContextVar("user_context", default={})
#
#
#
#     def load_user_info(user_id):
#         if not os.path.exists(os.path.join(RESPONSES_DIR, f"{user_id}", "user_info.csv")):
#             return None
#         df = pd.read_csv(os.path.join(RESPONSES_DIR, f"{user_id}", "user_info.csv"))
#         return df.iloc[0].to_dict()
#
#     def load_user_context():
#         for root, dirs, files in os.walk(RESPONSES_DIR):
#             for file in files:
#                 if file == "user_info.csv":
#                     user_id = int(os.path.basename(root))
#                     user_info = load_user_info(user_id)
#                     user_info["current_question_index"] = 0
#                     user_data = user_context.get()
#                     user_data[user_id] = user_info
#                     user_context.set(user_data)
#
#     def get_user_info(user_id):
#         user_data = user_context.get()
#         return user_data.get(user_id)
#
#     def get_user_info_field(user_id, field):
#         user_info = get_user_info(user_id)
#         field_value = user_info.get(field)
#         if field == "user_id" or field == "age":
#             return int(field_value)
#         else:
#             return field_value
#
#     def set_user_info_field(user_id, field, value):
#         user_data = user_context.get()
#         user_info = user_data.get(user_id)
#         user_info[field] = value
#         user_data[user_id] = user_info
#         user_context.set(user_data)
#
#     def add_new_user(user_id):
#         user_data = user_context.get()
#         user_data[user_id] = {"user_id": user_id,"gender": None,"age": None,"language": None,"current_question_index": 0}
#         user_context.set(user_data)
#
# load_user_context()
#
#
