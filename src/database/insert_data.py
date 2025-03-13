from sqlalchemy import insert
from sqlalchemy.engine import Connection

from src.database.db_connection import get_connection
from src.database.load_db_metadata import load_metadata
from src.database.select_data import select_id
from src.exception import CustomException
from src.logger import logger
from src.utils import multiply_dicts

from typing import List, Dict, Optional

import sys

def insert_rows(table_name: str, json: List[Dict], one_by_one: bool = True, get_pk: bool = True, connection: Optional[Connection]=None):
    '''
    Inserts new rows into a table in the database.
    '''
    
    engine = get_connection()   # Get engine
    metadata = load_metadata()
    table = metadata.tables[table_name]
    
    inserted_ids = []

    # Open connection with the db and insert a row into the table
    try:
        # Reuse connection if provided; otherwise, start a new transaction
        if connection:
            _execute_insert(table, json, one_by_one, get_pk, inserted_ids, connection)
        else:
            with engine.begin() as connection:
                _execute_insert(table, json, one_by_one, get_pk, inserted_ids, connection)
        
    
        logger.info(f"Row(s) inserted succesfully in *{table_name}* table.")
        return inserted_ids
    
    except Exception as e:
        raise CustomException(e, sys)
        

def _execute_insert(table, json, one_by_one, get_pk, inserted_ids, connection: Connection):
    '''
    Executes the actual logic.
    '''
    insert_query = insert(table)

    if one_by_one:
        for data in json:
            result_one = connection.execute(insert_query, data)
            if get_pk:
                inserted_ids.append(result_one.inserted_primary_key[0])

    else:
        result = connection.execute(insert_query, json)
        if get_pk:
            inserted_ids.extend([pk[0] for pk in result.inserted_primary_key_rows])

        

def insert_rows_dinamically(table_name:str, columns:List[str], ref_tables_name:List[str], ref_columns:List[str], json:List[Dict], connection_tables:List[str]):
    '''
    This function inserts new rows into a table dinamically, when this table has one or more foreign keys.
    Adds data to the table if the referenced columns has values or add a value into the referenced table first.
    '''
    engine = get_connection()

    try:
        # Start a new connection with a starting transaction
        with engine.begin() as connection:
            # Json to be added into the main table
            new_json = []
            
            # For each dict in json, appends new keys-values for inserting into the main table
            for dict_ in json:
                new_dict_ = dict_.copy()

                # For each referenced table performs the changes in the dict
                for ref_table_name, ref_column, column in zip(ref_tables_name, ref_columns, columns):
                    
                    ref_column_in_json = ref_column[0]
                    ref_column_in_ref = ref_column[1]
                    
                    # Gets the id if exists the ref_colum value in the referenced table 
                    id = select_id(ref_table_name, ref_column_in_ref, new_dict_[ref_column_in_json])

                    # Changes the key-value pair when id exists or not exists
                    if id:
                        new_dict_[column] = id[0]

                    else:
                        json_for_reftable = []
                        ref_value = new_dict_[ref_column_in_json]

                        if type(ref_value) == list:
                            json_for_reftable = [{ref_column_in_ref : ref_value_i} for ref_value_i in ref_value]
                        else:
                            json_for_reftable = [{ref_column_in_ref : ref_value}]    
                        print(ref_table_name)
                        new_ids = insert_rows(ref_table_name, json_for_reftable, connection=connection) # Adds data into the referenced table and gets the ids

                        if len(new_ids) == 1:
                            new_dict_[column] = new_ids[0]
                        else:
                            new_dict_[column] = new_ids
                
                # Adds the dictionary with keys-values added into the new json 
                new_json.append(new_dict_)
                print(new_json)

            main_ids = insert_rows(table_name, new_json, connection=connection) # Inserts the new json into the main table
            con_ids = [{'offer_id' : offer_id, 'career_id': list_careers_id} for offer_id, list_careers_id in zip(main_ids, [ dict_['career_id'] for dict_ in new_json ])] 

            print(con_ids)
            insert_rows(connection_tables, multiply_dicts(con_ids), get_pk=False, connection=connection)

        logger.info(f"Data insered into *{table_name}({str(ref_tables_name)})*")

    except Exception as e:
        raise CustomException(e, sys)