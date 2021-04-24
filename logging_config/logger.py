import logging


def get_logger():
    """
    This function used to configure logging.
    :return: It returns a logger. Using this logger we can put exceptions into log file.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)
    # Set logging format
    formatter = logging.Formatter('%(asctime)s : %(name)s : ', datefmt='%m/%d/%Y %I:%M:%S %p')
    # Adding exception.log file
    file_handler = logging.FileHandler('exceptions.log')
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
