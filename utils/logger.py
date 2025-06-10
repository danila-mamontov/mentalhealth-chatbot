import logging
import os
from datetime import datetime

class BotLogger:
    def __init__(self, base_dir="responses"):
        self.base_dir = base_dir

    def get_logger(self, user_id):
        """
        Creates a logger for a specific user and stores logs directly in their folder.
        :param user_id: Telegram user ID
        :return: Logger object
        """
        user_dir = os.path.join(self.base_dir, str(user_id))  # User's directory
        os.makedirs(user_dir, exist_ok=True)  # Create directory if it doesn't exist

        log_file = os.path.join(user_dir, "user.log")  # Log file directly in user's folder

        logger = logging.getLogger(f"User_{user_id}")  # Unique logger name
        if not logger.hasHandlers():  # Prevent duplicate handlers
            handler = logging.FileHandler(log_file, encoding="utf-8")
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)

        return logger

    def log_event(self, user_id, action, details=""):
        """
        Logs a user event in their individual log file.
        :param user_id: User ID
        :param action: Action performed (e.g., "START", "ANSWER_SURVEY")
        :param details: Additional details
        """
        logger = self.get_logger(user_id)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp} | Action: {action} | {details}"
        logger.info(log_message)

    def log_error(self, user_id, error_message):
        """
        Logs an error to the user's log file.
        :param user_id: User ID
        :param error_message: Error message
        """
        logger = self.get_logger(user_id)
        logger.error(f"ERROR: {error_message}")

    def close(self, user_id):
        """
        Closes the logger for a specific user.
        :param user_id: User ID
        """
        logger = self.get_logger(user_id)
        for handler in logger.handlers:
            handler.close()
            logger.removeHandler(handler)

logger = BotLogger()
