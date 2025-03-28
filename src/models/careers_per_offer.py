from src.database.load_db_metadata import load_table
from src.database.insert_data import insert_rows
from src.database.select_data import select_column, select_id

from src.logger import main_logger

class Careers_per_offer:

    def __init__(self):

        main_logger.info("Initializing Organizations class...")

        self.table_name = 'careers_per_offer'
        self.table = load_table(self.table_name)
        self.columns = self.table.columns.keys()

        main_logger.info(f"Careers_per_offer object initialized. Columns: {self.columns}.")
        

    def insert_rows(self, json, one_by_one=True):
        ids_inserted = insert_rows(self.table_name, json, one_by_one)
        return ids_inserted
    
    def select_column(self, column_name, limit=None):
        return select_column(self.table_name, column_name, limit)
    
    def select_id(self, col_value):
        return select_id(self.table_name, column_name='name', col_value=col_value)