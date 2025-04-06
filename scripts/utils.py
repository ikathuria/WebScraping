import sys
import json
import logging
from flask import Response


class CustomLogger:
    def __init__(self, name, log_file=None, level=logging.DEBUG):
        """
        Initializes the custom logger.

        Args:
            name (str): The name of the logger.
            log_file (str, optional): If specified, log output will be written to this file.
            level (int, optional): The logging level (default is INFO).
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Prevent adding handlers multiple times (important if reusing the logger)
        if not self.logger.handlers:
            log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            formatter = logging.Formatter(log_format)

            # Console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

            # File handler (if provided)
            if log_file:
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                file_handler.setLevel(level)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message, exception=None):
        """
        Logs error with optional traceback.

        Args:
            message (str): Custom error message.
            exception (Exception, optional): The exception to log with traceback.
        """
        if exception:
            self.logger.error(
                f"{message} | Exception: {exception}", exc_info=True)
        else:
            self.logger.error(message)


def render_json_data(data, status=200):
    return Response(json.dumps(data, indent=4), status=status, mimetype='application/json')
