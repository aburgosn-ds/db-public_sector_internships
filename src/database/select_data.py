from sqlalchemy import select
from src.database.db_connection import get_connection
from src.database.load_db_metadata import load_metadata
from src.exception import CustomException
from src.logger import logger

import sys

def select_column(table_name, column_name, limit=None):
    '''
    This function selects all column rows from a table from the database
    '''
    engine = get_connection() # Get engine
    metadata = load_metadata()
    table = metadata.tables[table_name]

    # Opens a connection with the db and selects the column values
    with engine.connect() as connection:
        try:
            select_query = select(table.c[column_name]).limit(limit)

            # Executes the query and gets the output
            result = connection.execute(select_query).fetchall()
            logger.info(f"{len(result)} rows where succesfully selected from *{table_name}({column_name})*")
            return result

        except Exception as e:
            raise CustomException(e, sys)


def select_id(table_name, column_name, col_value, limit=None):
    '''
    This function selects the id(s) from a table whose column value is col_value
    '''
    engine = get_connection() # Get engine
    metadata = load_metadata()
    table = metadata.tables[table_name]

    # Opens a connection with the db and performs operations 
    with engine.connect() as connection:
        try:
            # Selects id with condition
            if type(col_value) == list:
                select_query = select(table.c.id).where(table.c[column_name].in_(col_value)).limit(limit)

            elif type(col_value) == str:
                select_query = select(table.c.id).where(table.c[column_name] == col_value).limit(limit)

            # Executes the query and gets the output
            result = connection.execute(select_query).fetchall()
            logger.info(f"ID from table -{table_name}- searched successfully. Value to match: {col_value}")
            
            # Get the output as a list of tuples
            if len(result) > 0:
                result = [res._tuple()[0] for res in result]

            return result

        except Exception as e:
            logger.info(f"Error while selecting ID from table {table_name}. Value to match: {col_value}")
            raise CustomException (e, sys)