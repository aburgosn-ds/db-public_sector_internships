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
PORT = '3306'
DATABASE = 'public_sector_internships'


def get_connection():
    '''
    Gets the engine connection
    '''
    # URL for database connection
    DATABASE_URL = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

    # Create engine for connection
    engine = create_engine(DATABASE_URL)
    
    # Check the engine working properly
    try:
        connection =  engine.connect()
        connection.close()
        logger.info("Database engine connection created successfully and working properly")

        return engine
    
    except Exception as e:
        raise CustomException(e, sys)
    

if __name__ == "__main__":
    a = get_connection()
    print(a)