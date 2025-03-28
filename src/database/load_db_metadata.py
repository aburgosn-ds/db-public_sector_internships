from sqlalchemy import MetaData
from src.database.db_connection import get_connection
from src.exception import CustomException
from src.logger import logger

import sys

def load_metadata(engine = None):
    '''
    This function loads the database and returns the metadata
    '''
    # Get engine if not provided
    if not engine:
        engine = get_connection()
        
    try:
        metadata = MetaData()
        metadata.reflect(bind=engine) # Load all tables present in the db
        logger.info("Database tables metadata loaded.")
        
        return metadata

    except Exception as e:
        logger.error("Error reading metadata.", exc_info=True)
        raise CustomException(e, sys)


def load_table(table_name, engine=None):
    '''
    Loads table from metadata to a Table object.
    '''
    logger.info(f"Loading {table_name} table...")

    table = load_metadata(engine=engine).tables[table_name]

    logger.info(f"{table_name} table loaded.")

    return table