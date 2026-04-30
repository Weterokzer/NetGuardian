import logging
import os
from datetime import datetime


class Logger:
    """Логирование событий"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup()
        return cls._instance

    def _setup(self):
        log_dir = os.path.expanduser("~/.netguardian_logs")
        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(log_dir, f"netguardian_{datetime.now().strftime('%Y%m%d')}.log")

        self.logger = logging.getLogger('NetGuardian')
        self.logger.setLevel(logging.DEBUG)

        # Файловый обработчик
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        # Формат
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

    def debug(self, message):
        self.logger.debug(message)