import logging

import streamlit as st
import utils.constants as constants

logging_level = logging.DEBUG if constants.DEBUG else logging.INFO


def setup_logger(name: str, level: int = logging_level) -> logging.Logger:
    """Set up a logger with the specified name and level.

    Configures a logger with a stream handler and formatter. If a handler
    already exists, the logger is returned as-is to avoid duplicate logs.


    Args:
        name (str): The name of the logger.
        level (int): The logging level. Defaults to the logging_level variable.


    Returns:
        logging.Logger: A configured logger instance.


    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


@st.cache_resource
def get_logger(name: str, level: int = logging_level) -> logging.Logger:
    """Get a cached logger instance."""
    return setup_logger(name, level)


logger = get_logger(__name__)
