import os
import sys

from dotenv import load_dotenv
from sqlalchemy import create_engine
from src.exception import CustomException
from src.logger import logger


# Load environment variables
load_dotenv()

# Connection variables
USERNAME = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')
HOST = os.getenv('DB_HOST')
PORT = os.getenv('DB_PORT')
DATABASE = os.getenv('DB_NAME')


def get_connection():
    '''
    Gets the connection engine
    '''
    # URL for database connection
    DATABASE_URL = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

    
    # Check the engine working properly
    try:
        # Create engine for connection
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as connection:
            logger.info("Database engine connection created successfully and working properly")

        return engine
    
    except Exception as e:
        logger.error(f"Database test connection error: {e}", exc_info=True)
        raise CustomException(e, sys)