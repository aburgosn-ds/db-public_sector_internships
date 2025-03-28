import logging
import os
from datetime import datetime

# Root directory for logs
LOGS_BASE_DIR = os.path.join(os.getcwd(), "logs")

def get_logger(name, log_subdir='main'):
    """
    Create and return a logger with an own handler.
    """
    log_dir = os.path.join(LOGS_BASE_DIR, log_subdir)
    os.makedirs(log_dir, exist_ok=True)

    log_filename = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" if log_subdir == 'main' else 'scheduler.log'
    log_filepath = os.path.join(log_dir, log_filename)

    logger = logging.getLogger(name)

    # If the logger already has handlers, return it to prevent duplicates
    if logger.hasHandlers():
        return logger
    
    logger.setLevel(logging.INFO)
    
    # Create file handler
    file_handler = logging.FileHandler(log_filepath)
    file_handler.setFormatter(logging.Formatter("[ %(asctime)s ] %(name)s %(module)s %(filename)s %(lineno)d - %(levelname)s - %(message)s"))
    logger.addHandler(file_handler)

    return logger


# Logger for main execution
main_logger = get_logger('main_logger', 'main')

# Logger for the scheduler
scheduler_logger = get_logger('scheduler_logger', 'scheduler')