from src.database.load_db_metadata import load_metadata
from src.database.insert_data import insert_rows
from src.database.select_data import select_column

from src.logger import main_logger
from src.exception import CustomException


metadata = load_metadata()
class Location:

    def __init__(self):
        self.table_name = 'specific_locations'
        self.table = metadata.tables[self.table_name]
        self.columns = self.table.columns.keys()

    def insert_rows(self, json):
        insert_rows(self.table, json)
    
    def select_column(self, column_name, limit=None):
        return select_column(self.table, self.table_name, column_name, limit)