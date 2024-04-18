from loguru import logger
import os
import sys
import traceback


def find_project_root_folder(current_path):
    while not os.path.exists(os.path.join(current_path, "model")):
        parent = os.path.dirname(current_path)
        if parent == current_path:
            raise RuntimeError("Unable to find the project root.")
        current_path = parent
    return current_path


def setup_loguru_logger():
    logger.remove()
    project_root = find_project_root_folder(os.path.dirname(os.path.abspath(__file__)))
    log_file_path = os.path.join(project_root, "logs", "allps_service.log")
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS ZZ}</green> | <level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>{exception}"
    )
    logger.add(log_file_path, rotation="00:00", level="INFO", format=log_format, backtrace=True, diagnose=True)
    logger.add(sys.stderr, level="INFO", format=log_format, colorize=True, backtrace=True, diagnose=True)


def handle_exception(exc_type, exc_value, exc_traceback):
    """Global exception handler to catch and log any uncaught exceptions:"""
    # Allow program to exit without logging an error when KeyboardInterrupt is raised
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
    else:
        traceback_string = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        logger.error(
            f"An unhandled exception occurred: {exc_type.__name__}: {exc_value}, traceback: {traceback_string}"
        )


sys.excepthook = handle_exception
setup_loguru_logger()
