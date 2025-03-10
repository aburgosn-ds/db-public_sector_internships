from sqlalchemy import MetaData
from src.database.db_connection import get_connection
from src.exception import CustomException
from src.logger import logger

import sys

# Get engine
engine = get_connection()

# 
def load_metadata():
    '''
    This functin loads and returns the database metadata
    '''
    try:
        metadata = MetaData()
        metadata.reflect(bind=engine) # Load all tables present in the db
        logger.info("Database tables reading done")
        
        return metadata

    except Exception as e:
        raise CustomException(e, sys)
