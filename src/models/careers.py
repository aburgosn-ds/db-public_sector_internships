from src.database.load_db_metadata import load_table
from src.database.insert_data import insert_rows
from src.database.select_data import select_column

from src.logger import main_logger


class Careers:

    def __init__(self):

        main_logger.info("Initializing Careers class...")

        self.table_name = 'careers'
        self.table = load_table(self.table_name)
        self.columns = self.table.columns.keys()

        main_logger.info(f"Careers object initialized. Columns: {self.columns}.")


    def insert_rows(self, json, one_by_one, get_pk):
        insert_rows(self.table, json, one_by_one, get_pk)
    
    def select_column(self, column_name, limit=None):
        return select_column(self.table, self.table_name, column_name, limit)