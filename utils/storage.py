import os
import pandas as pd
from contextvars import ContextVar

# Create a new class UserContext that inherits from ContextVar
def load_user_info(user_id):
    from config import RESPONSES_DIR
    if not os.path.exists(os.path.join(RESPONSES_DIR, f"{user_id}", "user_info.csv")):
        return None
    df = pd.read_csv(os.path.join(RESPONSES_DIR, f"{user_id}", "user_info.csv"))
    return df.iloc[0].to_dict()


class UserContext:
    def __init__(self):
        self.contextVar = ContextVar("user_context", default={})

    def add_new_user(self, user_id):
        from survey import phq9_survey

        user_data = self.contextVar.get()

        params = {"user_id": user_id,
                  "gender": None,
                  "age": None,
                  "language": None,
                  "first_name": None,
                  "family_name": None,
                  "username": None,
                  "latitude": None,
                  "longitude": None,
                  "current_question_index": 0}

        for i in range(len(phq9_survey['en'])):
            params[f"phq9_{i}"] = None

        user_data[user_id] = params
        self.contextVar.set(user_data)

    def load_user_context(self):
        from config import RESPONSES_DIR

        for root, dirs, files in os.walk(RESPONSES_DIR):
            for file in files:
                if file == "user_info.csv":
                    user_id = int(os.path.basename(root))
                    user_info = load_user_info(user_id)
                    user_info["current_question_index"] = 0
                    user_data = self.contextVar.get()
                    user_data[user_id] = user_info
                    self.contextVar.set(user_data)

    def get_user_info(self, user_id):
        user_data = self.contextVar.get()
        return user_data.get(user_id)

    def get_user_info_field(self, user_id, field):
        user_info = self.get_user_info(user_id)
        field_value = user_info.get(field)
        if field == "user_id" or field == "age" or field == "current_question_index":
            return int(field_value)
        else:
            return str(field_value)

    def set_user_info_field(self, user_id, field, value):
        user_data = self.contextVar.get()
        user_info = user_data.get(user_id)
        user_info[field] = value
        user_data[user_id] = user_info
        self.contextVar.set(user_data)

    def save_user_info(self, user_id):
        from config import RESPONSES_DIR

        user_data = self.contextVar.get()
        user_info = user_data.get(user_id)
        gender = user_info["gender"]
        age = user_info["age"]
        language = user_info["language"]
        first_name = user_info["first_name"]
        family_name = user_info["family_name"]
        username = user_info["username"]
        latitude = user_info["latitude"]
        longitude = user_info["longitude"]

        df_user_info = pd.DataFrame(columns=['user_id','gender','age','language','first_name','family_name','username','latitude','longitude'],
                                    data=[[user_id,gender,age,language,first_name,family_name,username,latitude,longitude]])
        if age is not None:
            df_user_info = df_user_info.astype({'user_id': 'int64','gender': 'object','age': 'int64','language': 'object','first_name': 'object','family_name': 'object','username': 'object','latitude': 'float64','longitude': 'float64'})
        else:
            df_user_info = df_user_info.astype({'user_id': 'int64','gender': 'object','age': 'object','language': 'object','first_name': 'object','family_name': 'object','username': 'object','latitude': 'float64','longitude': 'float64'})
        df_user_info.to_csv(os.path.join(RESPONSES_DIR, str(user_id),"user_info.csv"), index=False)

    def save_phq9_info(self, user_id):
        from config import RESPONSES_DIR
        from survey import phq9_survey, get_phq9_question_from_id

        user_data = self.contextVar.get()
        user_info = user_data.get(user_id)
        phq9_info = {"user_id": user_id}

        for i in range(len(phq9_survey['en'])):
            phq9_info[f"phq9_{i}"] = user_info[f"phq9_{i}"]
        df_phq9_info = pd.DataFrame.from_dict(phq9_info, orient='index').T
        df_phq9_info.to_csv(os.path.join(RESPONSES_DIR, str(user_id), f"survey_PHQ9.csv"), index=False)

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
