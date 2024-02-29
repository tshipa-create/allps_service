import logging
import os
from logging.handlers import TimedRotatingFileHandler


# So logging would work from tests directory or main directory
# Needs some static folder to find the initial project root path. That's why we are using "model" folder
def find_project_root_folder(current_path):
    while not os.path.exists(os.path.join(current_path, "model")):
        parent = os.path.dirname(current_path)
        if parent == current_path:
            raise RuntimeError("Unable to find the project root.")
        current_path = parent
    return current_path


project_root = find_project_root_folder(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE_PATH = os.path.join(project_root, "logs", "allps_service.log")
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

logging.basicConfig(
    format="%(levelname)s - %(asctime)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        TimedRotatingFileHandler(LOG_FILE_PATH, when="midnight"),
    ],
    level="WARNING",
)

logObject = logging.getLogger()
