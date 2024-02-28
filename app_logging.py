import logging


logging.basicConfig(
    format="%(levelname)s - %(asctime)s - %(message)s",
    handlers=[logging.StreamHandler()],
    level="WARNING",
)

logObject = logging.getLogger()
