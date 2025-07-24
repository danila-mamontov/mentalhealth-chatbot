import logging
import os
from datetime import datetime
from utils.db import insert_log
from utils.storage import context

class BotLogger:
    def __init__(self, base_dir="responses"):
        self.base_dir = base_dir

    def get_logger(self, t_id):
        """
        Creates a logger for a specific user and stores logs directly in their folder.
        :param t_id: Telegram user ID
        :return: Logger object
        """
        uid = context.get_user_info_field(t_id, "id")
        if uid is None:
            uid = t_id
        user_dir = os.path.join(self.base_dir, str(uid))  # User's directory
        os.makedirs(user_dir, exist_ok=True)  # Create directory if it doesn't exist

        log_file = os.path.join(user_dir, "user.log")  # Log file directly in user's folder

        logger = logging.getLogger(f"User_{t_id}")  # Unique logger name
        if not logger.hasHandlers():  # Prevent duplicate handlers
            handler = logging.FileHandler(log_file, encoding="utf-8")
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)

        return logger

    def log_event(self, t_id, action, details=""):
        """
        Logs a user event in their individual log file.
        :param t_id: Telegram user ID
        :param action: Action performed (e.g., "START", "ANSWER_SURVEY")
        :param details: Additional details
        """
        logger = self.get_logger(t_id)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp} | Action: {action} | {details}"
        logger.info(log_message)
        uid = context.get_user_info_field(t_id, "id")
        if uid is not None:
            insert_log(uid, timestamp, action, details)

    def log_error(self, t_id, error_message):
        """
        Logs an error to the user's log file.
        :param t_id: Telegram user ID
        :param error_message: Error message
        """
        logger = self.get_logger(t_id)
        logger.error(f"ERROR: {error_message}")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        uid = context.get_user_info_field(t_id, "id")
        if uid is not None:
            insert_log(uid, timestamp, "ERROR", error_message)

    def close(self, t_id):
        """
        Closes the logger for a specific user.
        :param t_id: Telegram user ID
        """
        logger = self.get_logger(t_id)
        for handler in logger.handlers:
            handler.close()
            logger.removeHandler(handler)

logger = BotLogger()
