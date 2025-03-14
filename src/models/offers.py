from src.database.load_db_metadata import load_metadata
from src.database.insert_data import insert_rows, insert_rows_dinamically
from src.database.select_data import select_column

from src.logger import logger
from src.exception import CustomException


class Offers:

    def __init__(self):
        self.table_name = 'offers'
        self.table = load_metadata().tables[self.table_name]
        self.columns = self.table.columns.keys()

    def insert_rows(self, json):
        insert_rows(self.table_name, json)

    def insert_rows_dinamically(self, json):
        insert_rows_dinamically(self.table_name, 
                                columns=['specific_location_id', 'city_id', 'organization_id', 'careers_id'], 
                                ref_tables_name=['specific_locations', 'cities', 'organizations', 'careers'], 
                                ref_columns=[('specific_location', 'address'), ('city', 'name'), ('organization', 'name'), ('careers', 'name')], 
                                json=json,
                                connection_table='careers_per_offer')
        
    def select_column(self, column_name, limit=None):
        return select_column(self.table_name, column_name, limit)