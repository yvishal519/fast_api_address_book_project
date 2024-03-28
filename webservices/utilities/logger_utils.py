import logging
import coloredlogs
from webservices.configs import app_configurations as app_config

# Create a logger
logger = logging.getLogger(__name__)

# Set the log level to DEBUG
logger.setLevel(logging.DEBUG)

# Create a formatter for console logging
console_formatter = coloredlogs.ColoredFormatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                                 level_styles={'debug': {'color': 'blue'}, 'info': {'color': 'green'},
                                                               'warning': {'color': 'yellow'},
                                                               'error': {'color': 'red'}})


# Create a console handler and set the formatter
if app_config.CONSOLE_LOG_ENABLED:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

# Create a formatter for file logging (without ANSI characters)
file_formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# File logging configuration

if app_config.FILE_LOG_ENABLED:
    file_handler = logging.FileHandler(app_config.LOG_FILE_NAME)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


# Optionally, you can add context information to log messages
def log_with_context(message, context=None):
    if context:
        logger.info("%s - %s", message, context)
    else:
        logger.info(message)
