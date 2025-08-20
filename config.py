import os

API_URL = "http://134.60.124.44:8081/bot{0}/{1}"
LOCAL_SERVER_MODE = os.getenv("LOCAL_SERVER_MODE", "false").lower() in ("true", "1", "yes")
BOT_TOKEN = os.getenv("BOT_TOKEN")
RESPONSES_DIR = "responses"
STATS_PATH = "stats.csv"
DB_PATH = os.getenv("DB_PATH", os.path.join(RESPONSES_DIR, "bot.db"))

if not os.path.exists(RESPONSES_DIR):
    os.makedirs(RESPONSES_DIR)

