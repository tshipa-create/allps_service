from loguru import logger
import os
import sys


def find_project_root_folder(current_path):
    while not os.path.exists(os.path.join(current_path, "model")):
        parent = os.path.dirname(current_path)
        if parent == current_path:
            raise RuntimeError("Unable to find the project root.")
        current_path = parent
    return current_path


def setup_loguru_logger():
    if not logger._core.handlers:  # This checks if any handlers are already attached to the logger
        project_root = find_project_root_folder(os.path.dirname(os.path.abspath(__file__)))
        log_file_path = os.path.join(project_root, "logs", "allps_service.log")
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

        logger.add(
            log_file_path, rotation="00:00", level="WARNING", format="{time:YYYY-MM-DD HH:mm:ss} - {level} - {message}"
        )
        logger.add(sys.stdout, level="WARNING", format="{time:YYYY-MM-DD HH:mm:ss} - {level} - {message}")


setup_loguru_logger()
