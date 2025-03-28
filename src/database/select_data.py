from sqlalchemy import select
from sqlalchemy import Table

from src.database.db_connection import get_connection
from src.exception import CustomException
from src.logger import main_logger

import sys

def select_column(table_object, table_name, column_name, limit=None):
    '''
    This function selects all column rows from a table from the database
    '''

    main_logger.info(f"Selecting {column_name} column from {table_name} table...")

    engine = get_connection() # Get engine

    # Opens a connection with the db and selects the column values
    try:
        with engine.connect() as connection:
            select_query = select(table_object.c[column_name]).limit(limit)

            # Executes the query and gets the output
            result = connection.execute(select_query).fetchall()
            main_logger.info(f"{len(result)} rows where succesfully selected from {column_name} column in {table_name} table.")
            return result

    except Exception as e:
        main_logger.error(f"Error while fetching the column {column_name} from {table_name} table: {e}")
        raise CustomException(e, sys)


def select_id(table_object: Table, column_name: str, col_value: str, limit: int=None):
    '''
    This function selects the id(s) from a table whose column value is col_value argument
    '''
    table_name = table_object.name
    main_logger.info(f"Selecting ids that matches {col_value} in {column_name} column from {table_name} table...")
    
    engine = get_connection() # Get engine

    # Opens a connection with the db and performs operations 
    try:
        with engine.connect() as connection:
            # Selects id with condition
            if col_value:
                if type(col_value) == list:
                    select_query = select(table_object.c.id).where(table_object.c[column_name].in_(col_value)).limit(limit)

                elif type(col_value) == str:
                    select_query = select(table_object.c.id).where(table_object.c[column_name] == col_value).limit(limit)
            else:
                return []

            # Executes the query and gets the output: list of tuples
            result = connection.execute(select_query).fetchall()
            
            # Get the output as a list of ids only
            if len(result) > 0:
                result = [res._tuple()[0] for res in result]

            main_logger.info(f"Id(s) from {column_name} column in {table_name} table found successfully: {result}.")
            return result

    except Exception as e:
        main_logger.error(f"Error while selecting ID from table {table_name}. Value to match: {column_name}({col_value}). {e}")
        raise CustomException (e, sys)