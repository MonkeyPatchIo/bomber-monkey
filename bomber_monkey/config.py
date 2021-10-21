import logging

LOG_LEVEL = logging.INFO


def setup_logs():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=LOG_LEVEL
    )
