from src.database.load_db_metadata import load_metadata
from src.database.insert_data import insert_rows
from src.database.select_data import select_column

from src.logger import logger
from src.exception import CustomException


class Cities:

    def __init__(self):
        self.table_name = 'cities'
        self.table = load_metadata().tables[self.table_name]
        self.columns = self.table.columns.keys()

    def insert_rows(self, json):
        insert_rows(self.table_name, json)
    
    def select_column(self, column_name, limit=None):
        return select_column(self.table_name, column_name, limit)