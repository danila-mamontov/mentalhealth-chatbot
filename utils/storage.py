from localization import translations
from utils.db import (
    upsert_user_profile,
    upsert_phq_answers,
    get_connection,
    init_db,
    delete_user_records,
)

init_db()


def get_translation(t_id, key):
    language = context.get_user_info_field(t_id, "language")
    return translations[key].get(language)

# Database helpers
def load_user_info(t_id):
    conn = get_connection()
    cur = conn.execute("SELECT * FROM user_profile WHERE t_id=?", (t_id,))
    row = cur.fetchone()
    if row:
        return dict(row)
    return None

def get_user_profile(t_id):
    text = get_translation(t_id, "profile_template")

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
            translated = get_translation(t_id, val)
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

    def _ensure_session(self, uid):
        self._session.setdefault(uid, {
            "current_question_index": 0,
            "vm_ids": {},
            "message_to_del": None,
            "survey_message_id": None,
            "survey_controls_id": None,
        })

    def add_new_user(self, t_id):
        params = {
            "t_id": t_id,
            "consent": None,
            "gender": None,
            "age": None,
            "language": None,
            "treatment": None,
            "depressive": None,
        }

        upsert_user_profile(params)
        conn = get_connection()
        row = conn.execute("SELECT id FROM user_profile WHERE t_id=?", (t_id,)).fetchone()
        if row:
            uid = row["id"]
            self._tid_to_id[t_id] = uid
        else:
            uid = None

        # prepare ephemeral fields
        if uid is not None:
            self._session[uid] = {
                "current_question_index": 0,
                "vm_ids": {},
                "message_to_del": None,
                "survey_message_id": None,
                "survey_controls_id": None,
            }

    def delete_user(self, t_id):
        uid = self._tid_to_id.get(t_id)
        if uid is None:
            row = get_connection().execute("SELECT id FROM user_profile WHERE t_id=?", (t_id,)).fetchone()
            if row:
                uid = row["id"]
        if uid is not None:
            self._session.pop(uid, None)
            delete_user_records(uid)

    def load_user_context(self):
        """Placeholder for backward compatibility."""
        pass

    def _get_id(self, t_id):
        uid = self._tid_to_id.get(t_id)
        if uid is not None:
            return uid
        row = get_connection().execute("SELECT id FROM user_profile WHERE t_id=?", (t_id,)).fetchone()
        if row:
            uid = row["id"]
            self._tid_to_id[t_id] = uid
            return uid
        return None

    def _load_profile(self, t_id):
        conn = get_connection()
        cur = conn.execute("SELECT * FROM user_profile WHERE t_id=?", (t_id,))
        row = cur.fetchone()
        if row:
            self._tid_to_id[t_id] = row["id"]
        return dict(row) if row else None

    def get_user_info(self, t_id):
        profile = self._load_profile(t_id)
        if profile is None:
            return None
        uid = profile["id"]
        self._ensure_session(uid)
        profile.update(self._session[uid])
        return profile

    def get_user_info_field(self, t_id, field):
        if field in {"current_question_index", "vm_ids", "message_to_del", "survey_message_id", "survey_controls_id"}:
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
        if field in {"current_question_index", "vm_ids", "message_to_del", "survey_message_id", "survey_controls_id"} or field.startswith("phq_"):
            uid = self._get_id(t_id)
            if uid is None:
                return
            self._ensure_session(uid)
            self._session[uid][field] = value
            return

        conn = get_connection()
        conn.execute(f"UPDATE user_profile SET {field}=? WHERE t_id=?", (value, t_id))
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
        upsert_phq_answers(uid, answers)

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
