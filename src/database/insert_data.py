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

def insert_rows(table_name, json):
    '''
    This functions inserts new rows into a table in the database
    '''
    metadata = load_metadata()
    table = metadata.tables[table_name]
    
    with engine.connect() as connection:
        try:
            insert_query = insert(table)

            result = connection.execute(insert_query, json)
            connection.commit()

            logger.info(f"Row(s) inserted succesfully in *{table_name}* table. ID(s): {result.inserted_primary_key_rows}")

        except Exception as e:
            connection.rollback()
            raise CustomException(e, sys)
        

def insert_rows_dinamically(table_name:str, columns:List[str], ref_tables_name:List[str], ref_columns:List[str], json:List[Dict]):
    '''
    This function inserts new rows into a table dinamically, when this table has one or more foreign keys.
    Adds data if the referenced column has the value or add a value into the referenced table first.
    '''

    try:
        new_json = []
        
        for dict_ in json:
            new_dict_ = dict_.copy()
            for ref_table_name, ref_column, column in zip(ref_tables_name, ref_columns, columns):

                id = select_id(ref_table_name, ref_column, dict_[ref_column])

                if id:
                    new_dict_ = change_key_value(new_dict_, {ref_column:new_dict_[ref_column]}, {column: id[0]})

                else:
                    json_for_reftable = [{ref_column : new_dict_[ref_column]}]
                    insert_rows(ref_table_name, json_for_reftable)

                    new_id = select_id(ref_table_name, ref_column, dict_[ref_column])
                    new_dict_ = change_key_value(new_dict_, {ref_column:new_dict_[ref_column]}, {column: new_id[0]})
                

            new_json.append(new_dict_)
                
        insert_rows(table_name, new_json)
        logger.info(f"Data insered into *{table_name}* and *{ref_tables_name}* dinamically")

    except Exception as e:
        raise CustomException(e, sys)