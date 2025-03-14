from src.database.load_db_metadata import load_metadata
from src.database.insert_data import insert_rows
from src.database.select_data import select_column

from src.logger import logger
from src.exception import CustomException


class Careers:

    def __init__(self):
        self.table_name = 'careers'
        self.table = load_metadata().tables[self.table_name]
        self.columns = self.table.columns.keys()

    def insert_rows(self, json, one_by_one, get_pk):
        insert_rows(self.table_name, json, one_by_one, get_pk)
    
    def select_column(self, column_name, limit=None):
        return select_column(self.table_name, column_name, limit)