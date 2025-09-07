import logging

# create file handler which logs even debug messages
file_handler = logging.FileHandler('worker.log')
file_handler.setLevel(logging.DEBUG)

# create console handler with a higher log level
channel_handler = logging.StreamHandler()
channel_handler.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s '
                              '- %(message)s')
file_handler.setFormatter(formatter)
channel_handler.setFormatter(formatter)


def create_logger(logger_name, logger_level=logging.DEBUG):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logger_level)

    # add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(channel_handler)

    return logger
