import logging
import sys
import os


class Logger:
    """Singleton Logger class"""
    _instance = None
    directory = 'logs'
    file = 'errors.log'

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'logger'):
            self.logger = None
            self.setup_logging()

    def setup_logging(self):
        self.logger = logging.getLogger(__name__)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
        self.logger.setLevel(logging.ERROR)  # Set log level to ERROR

        # Console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # File
        log_dir = self.directory
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file = os.path.join(log_dir, self.file)

        self.logger.log_file = log_file
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def error(self, message):
        self.logger.error(message)
