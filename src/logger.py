import logging
import os
from datetime import datetime

LOG_FILENAME = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_DIRNAME = LOG_FILENAME

log_path = os.path.join(os.getcwd(), 'logs', LOG_DIRNAME)
os.makedirs(log_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(log_path, LOG_FILENAME)


logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(name)s %(module)s %(filename)s %(lineno)d - %(levelname)s - %(message)s",
    level=logging.INFO,
    force=True
)

# Create a new logger
logger = logging.getLogger('logger')