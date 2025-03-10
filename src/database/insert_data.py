from sqlalchemy import insert
from src.database.db_connection import get_connection
from src.database.load_db_metadata import load_metadata
from src.database.select_data import select_id
from src.exception import CustomException
from src.logger import logger
from src.utils import change_key_value

from typing import List, Dict

import sys

# Get engine
engine = get_connection()

def insert_rows(table_name, json: List[Dict]):
    '''
    This functions inserts new rows into a table in the database
    '''
    metadata = load_metadata()
    table = metadata.tables[table_name]
    
    # Open connection with the db and insert a row into the table
    with engine.connect() as connection:
        try:
            insert_query = insert(table)

            # Executes the query and commits if all ok
            result = connection.execute(insert_query, json)
            connection.commit()

            logger.info(f"Row(s) inserted succesfully in *{table_name}* table.")

        except Exception as e:
            # Rollbacks if there is an error
            connection.rollback()
            raise CustomException(e, sys)
        

def insert_rows_dinamically(table_name:str, columns:List[str], ref_tables_name:List[str], ref_columns:List[str], json:List[Dict]):
    '''
    This function inserts new rows into a table dinamically, when this table has one or more foreign keys.
    Adds data to the table if the referenced columns has values or add a value into the referenced table first.
    '''

    try:
        # Json to be added into the main table
        new_json = []
        
        # For each dict in json, changes the keys-values with appropriate ones for inserting into the main table
        for dict_ in json:
            new_dict_ = dict_.copy()

            # For each referenced table performs the changes in the dict
            for ref_table_name, ref_column, column in zip(ref_tables_name, ref_columns, columns):
                
                # Gets the id if exists of the ref_colum value in the referenced table 
                id = select_id(ref_table_name, ref_column, dict_[ref_column])

                # Changes the key-value pair when id exists or not exists
                if id:
                    new_dict_ = change_key_value(new_dict_, {ref_column:new_dict_[ref_column]}, {column: id[0]})

                else:
                    json_for_reftable = [{ref_column : new_dict_[ref_column]}]
                    insert_rows(ref_table_name, json_for_reftable) # Adds data into the referenced table

                    new_id = select_id(ref_table_name, ref_column, dict_[ref_column]) # Gets the id of the data inserted
                    new_dict_ = change_key_value(new_dict_, {ref_column:new_dict_[ref_column]}, {column: new_id[0]})
                
            # Adds the dictionary with keys-values changed into the new json 
            new_json.append(new_dict_)
                
        insert_rows(table_name, new_json) # Inserts the new json into the main table
        logger.info(f"Data insered into *{table_name}({str(ref_tables_name)})*")

    except Exception as e:
        raise CustomException(e, sys)