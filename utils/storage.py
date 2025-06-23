import os
from contextvars import ContextVar
from localization import translations
from utils import db


def get_translation(user_id,key):
    language = context.get_user_info_field(user_id, "language")
    return translations[key].get(language)

# Create a new class UserContext that inherits from ContextVar

def get_user_profile(user_id):
    text = get_translation(user_id, "profile_template")
    text = text.replace("{user_id}", str(user_id))
    text = text.replace("{age}", str(context.get_user_info_field(user_id, "age")))
    text = text.replace("{gender}", get_translation(user_id, context.get_user_info_field(user_id, "gender")))
    text = text.replace("{language}", context.get_user_info_field(user_id, "language"))
    return text


class UserContext:
    def __init__(self):
        self.contextVar = ContextVar("user_context", default={})

    def add_new_user(self, user_id):
        from survey import phq9_survey, WBMMS_survey

        user_data = self.contextVar.get()

        params = {"user_id": user_id,
                    "consent": None,
                  "gender": None,
                  "age": None,
                  "language": None,
                  "treatment": None,
                  "depressive": None,
                  "first_name": None,
                  "family_name": None,
                  "username": None,
                  "current_question_index": 0}

        for i in range(len(phq9_survey['en'])):
            params[f"phq_{i}"] = None

        for i in range(len(WBMMS_survey['en'])):
            params["vm_ids"] = dict()

        user_data[user_id] = params
        self.contextVar.set(user_data)
    def delete_user(self, user_id):
        self.contextVar.set({k: v for k, v in self.contextVar.get().items() if k != user_id})
    def load_user_context(self):
        """Load user info from the SQL database into the in-memory context."""
        from survey import phq9_survey, WBMMS_survey

        db.init_db()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        for row in rows:
            user_id = row["user_id"]
            user_info = dict(row)
            user_info["current_question_index"] = 0
            for i in range(len(phq9_survey['en'])):
                user_info[f"phq_{i}"] = None
            for qid, ans in conn.execute(
                "SELECT question_id, answer FROM phq_answers WHERE user_id=?",
                (user_id,),
            ):
                user_info[f"phq_{qid}"] = ans
            for _ in range(len(WBMMS_survey['en'])):
                user_info["vm_ids"] = dict()
            user_data = self.contextVar.get()
            user_data[user_id] = user_info
            self.contextVar.set(user_data)
        conn.close()

    def get_user_info(self, user_id):
        user_data = self.contextVar.get()
        return user_data.get(user_id)

    def get_user_info_field(self, user_id, field):
        user_info = self.get_user_info(user_id)
        field_value = user_info.get(field)
        if field == "user_id" or field == "age" or field == "current_question_index":
            if str(field_value) == "nan" or field_value is None:
                return None
            return int(field_value)
        else:
            return field_value


    def set_user_info_field(self, user_id, field, value):
        user_data = self.contextVar.get()
        user_info = user_data.get(user_id)
        user_info[field] = value
        user_data[user_id] = user_info
        self.contextVar.set(user_data)

    def save_user_info(self, user_id):
        """Persist user profile information to the database."""
        user_data = self.contextVar.get()
        user_info = user_data.get(user_id)

        db.upsert_user({
            "user_id": user_id,
            "consent": user_info["consent"],
            "gender": user_info["gender"],
            "age": user_info["age"],
            "language": user_info["language"],
            "treatment": user_info["treatment"],
            "depressive": user_info["depressive"],
            "first_name": user_info["first_name"],
            "family_name": user_info["family_name"],
            "username": user_info["username"],
            "latitude": user_info["latitude"],
            "longitude": user_info["longitude"],
        })

    def save_phq_info(self, user_id):
        """Save PHQ-9 answers for a user into the database."""
        from survey import phq9_survey

        user_data = self.contextVar.get()
        user_info = user_data.get(user_id)
        answers = {}
        for i in range(len(phq9_survey['en'])):
            answers[i] = user_info.get(f"phq_{i}")
        db.save_phq_answers(user_id, answers)

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
