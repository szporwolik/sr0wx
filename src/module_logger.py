# -*- coding: utf-8 -*-

"""Module to keep all the logging and CLI interface
   actrivities.
"""

import logging
from src import module_constants

# Logging configuration
def setup_logging(config):
    # create formatter and add it to the handlers
    formatter = logging.Formatter(config.log_line_format)

    # Creating logger with the lowest log level in config handlers
    min_log_level = min([h['log_level'] for h in config.log_handlers])
    
    logger = logging.getLogger()
    logger.setLevel(min_log_level)

    # create logging handlers according to its definitions
    for handler_definition in config.log_handlers:
        handler = handler_definition['class'](**handler_definition['config'])
        handler.setLevel(handler_definition['log_level'])
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

def text_color(color,text):
    text = color + text + module_constants.COLOR_ENDC
    return text
    