import logging
import os

class ScalpelLogger:
    """
    The logger logs messages both to the console and a file named checker.log by default. 
    The console handler is set to log messages of level INFO and above (i.e., INFO, WARNING, ERROR, etc.).
    The file handler logs all messages including DEBUG level.
    The ScalpelLogger class provides methods like log_info, log_warning, log_error, and log_debug to log messages of different levels.
    """
    def __init__(self, log_file_name="checking.log"):
        # Set up logger
        self.logger = logging.getLogger('Checker')
        self.logger.setLevel(logging.DEBUG)

        # Create file handler which logs even debug messages
        file_handler = logging.FileHandler(log_file_name)
        file_handler.setLevel(logging.DEBUG)

        # Create console handler with a higher log level (e.g. INFO)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add the handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_debug(self, message):
        self.logger.debug(message)

# Usage
logger = ScalpelLogger()

# Sample logging
logger.log_info("This is an informational message.")
logger.log_warning("This is a warning.")
logger.log_error("This is an error!")
logger.log_debug("This is a debug message.")  # This will only be logged to the file.
