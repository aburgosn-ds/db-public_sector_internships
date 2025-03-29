from sqlalchemy import insert
from sqlalchemy.engine import Connection
from sqlalchemy import Table

from src.database.db_connection import get_connection
from src.database.load_db_metadata import load_table
from src.database.db_connection import get_connection
from src.database.select_data import select_id
from src.exception import CustomException
from src.logger import main_logger

from typing import List, Dict, Optional

import sys

def insert_rows(table_object: Table, json: List[Dict], one_by_one: bool = True, get_pk: bool = True, connection: Optional[Connection]=None):
    '''
    Inserts new rows into a table in the database.
    '''
    engine = get_connection()
    table_name = table_object.name
    
    inserted_ids = []

    try:
        # Reuse connection if provided; otherwise, start a new transaction
        if connection:
            _execute_insert(table_object, json, one_by_one, get_pk, inserted_ids, connection)
        else:
            with engine.begin() as connection:
                _execute_insert(table_object, json, one_by_one, get_pk, inserted_ids, connection)
        
    
        main_logger.info(f"Row(s) inserted succesfully in *{table_name}* table. Inserted id(s): {inserted_ids}")
        return inserted_ids
    
    except Exception as e:
        main_logger.error(f"Error while inserting data into {table_name} table: ", exc_info=True)
        raise CustomException(e, sys)
        

def _execute_insert(table_object, json, one_by_one, get_pk, inserted_ids, connection: Connection):
    '''
    Executes the actual logic.
    '''
    insert_query = insert(table_object)

    if one_by_one:
        for data in json:
            try:
                result_one = connection.execute(insert_query, data)
                if get_pk:
                    inserted_ids.append(result_one.inserted_primary_key[0])
            except Exception as e:
                main_logger.warning(f"Error while inserting one row into {table_object.name} table: {e}. Skipping...")

    else:
        result = connection.execute(insert_query, json)
        if get_pk:
            inserted_ids.extend([pk[0] for pk in result.inserted_primary_key_rows])

        
def insert_rows_dinamically(main_table: Table, columns: List[str], ref_tables: List[Table], ref_columns: List[str], json: List[Dict], connection_tables: List[Table]):
    '''
    Inserts new rows into a table dinamically, when this table has one or more foreign keys.
    Adds data to the table if the referenced columns has values or add a value into the referenced table first.
    '''
    engine = get_connection()
    main_table_name = main_table.name
    connection_tables_names = [connection_table.name for connection_table in connection_tables]

    try:
        # Start a new connection with a starting transaction
        failed_inserts = [] # Keep track of unsuccessful inserts
        success_inserts = [] # Keep track of successful inserts
        new_json = [] # Json to be added into the main table

        
        # For each dict in json, appends new keys-values and insert them into the main table
        for dict_ in json:
            with engine.connect() as connection:

                # Capture and passes insert errors for each row
                try:
                    new_dict_ = dict_.copy()

                    # For each referenced table performs the addition in the dict
                    for ref_table, ref_column, column in zip(ref_tables, ref_columns, columns):
                            
                        ref_column_in_json = ref_column[0]
                        ref_column_in_ref = ref_column[1]
                            
                        # Gets the id if exists the ref_colum value in the referenced table 
                        id = select_id(ref_table, ref_column_in_ref, new_dict_[ref_column_in_json])

                        # Add key-value pairs if id exists or not exists
                        if id:
                            if ref_table.name not in connection_tables_names[0]:
                                new_dict_[column] = id[0]
                            else:
                                new_dict_[column] = id
                                
                        else:
                            json_for_reftable = []
                            ref_value = new_dict_[ref_column_in_json]

                            if type(ref_value) == list:
                                json_for_reftable = [{ref_column_in_ref : ref_value_i} for ref_value_i in ref_value]
                            else:
                                json_for_reftable = [{ref_column_in_ref : ref_value}]    

                            new_ids = insert_rows(ref_table, json_for_reftable, connection=connection) # Adds data into the referenced table and gets the ids

                            if ref_table.name not in connection_tables_names[0]:
                                new_dict_[column] = new_ids[0]
                            else:
                                new_dict_[column] = new_ids
                        
                    offer_id = insert_rows(main_table, [new_dict_], connection=connection)[0]
                    conn_json = [{'offer_id': offer_id, 'career_id': career_id} for career_id in new_dict_['careers_id']]
                    insert_rows(connection_tables[0], conn_json, get_pk=False, connection=connection)

                    connection.commit()

                    success_inserts.append(offer_id)

                    # Adds the dictionary with keys-values added into the new json 
                    new_json.append(new_dict_)
                    main_logger.info(f"Row inserted dynamically in all tables. Main table{main_table_name}, id: {offer_id}")
                    # print(f"Done. Id: {offer_id}")

                except Exception as e:
                    connection.rollback()
                    failed_inserts.append({'offer_page_code': new_dict_['offer_page_code'], 'url': new_dict_['url']})
                    main_logger.warning(f"Rollback. Error while inserting one row into *{main_table_name}* table dinamically. Page code: {new_dict_['offer_page_code']}. Url: {new_dict_['url']}. {e}", exc_info=True)

        main_logger.info(f"Data inserted successfully and dynamically into *{main_table_name}* table.\n\tIds:\n\t\tSuccessful inserts: {success_inserts}.\n\t\tUnsuccessful inserts: {failed_inserts}.")
        return failed_inserts

    except Exception as e:
        main_logger.error(f"Error database transaction into {main_table_name} table: ", exc_info=True)
        raise CustomException(e, sys)