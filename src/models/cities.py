from src.database.load_db_metadata import load_table
from src.database.insert_data import insert_rows
from src.database.select_data import select_column

from src.logger import main_logger


class Cities:

    def __init__(self):

        main_logger.info("Initializing Cities class...")

        self.table_name = 'cities'
        self.table = load_table(self.table_name)
        self.columns = self.table.columns.keys()

        main_logger.info(f"Cities object initialized. Columns: {self.columns}.")

    def insert_rows(self, json):
        insert_rows(self.table_name, json)
    
    def select_column(self, column_name, limit=None):
        return select_column(self.table_name, column_name, limit)