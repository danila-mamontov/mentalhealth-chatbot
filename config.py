import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
RESPONSES_DIR = "responses"
STATS_PATH = "stats.csv"
DB_PATH = os.getenv("DB_PATH", os.path.join(RESPONSES_DIR, "bot.db"))
ID_DB_PATH = os.getenv("ID_DB_PATH", os.path.join(RESPONSES_DIR, "id_map.db"))

if not os.path.exists(RESPONSES_DIR):
    os.makedirs(RESPONSES_DIR)

