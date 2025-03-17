from sqlalchemy import MetaData
from src.database.db_connection import get_connection
from src.exception import CustomException
from src.logger import logger

import sys

def load_metadata(engine = None):
    '''
    This function loads and returns the database metadata
    '''
    # Get engine if not provided
    if not engine:
        engine = get_connection()
        
    try:
        metadata = MetaData()
        metadata.reflect(bind=engine) # Load all tables present in the db
        logger.info("Database tables reading done")
        
        return metadata

    except Exception as e:
        logger.info("Error reading metadata.")
        raise CustomException(e, sys)
