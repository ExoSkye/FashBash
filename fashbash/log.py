import logging

import config

logger = logging.getLogger("discord")

def configure_logger():
    """
    Sets up the logger.
    """
    # The reason we call this function instead of setting it up outside of it
    # is because of the config.get_config() call, and the config could 
    # potentially be not set up yet when this code runs from an import.
    logger.setLevel(config.get_config("log_level"))
    formatter = logging.Formatter(
        "%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    file_handler = logging.FileHandler(
        filename="discord.log", encoding="utf-8", mode="w")
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)