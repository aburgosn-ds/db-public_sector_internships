from src.database.load_db_metadata import load_table
from src.database.insert_data import insert_rows, insert_rows_dinamically
from src.database.select_data import select_column

from src.models.organizations import Organizations
from src.models.cities import Cities
from src.models.careers import Careers
from src.models.careers_per_offer import Careers_per_offer

from src.logger import main_logger


class Offers:

    def __init__(self):

        main_logger.info("Initializing Offers class...")

        self.table_name = 'offers'
        self.table = load_table(self.table_name)
        self.columns = self.table.columns.keys()

        main_logger.info(f"Offers object initialized. Columns: {self.columns}.")

    def insert_rows(self, json):
        insert_rows(self.table, self.table_name, json)

    def insert_rows_dinamically(self, json):
        
        return insert_rows_dinamically(
                                self.table,
                                columns=['city_id', 'organization_id', 'careers_id'], 
                                ref_tables=[Cities().table, Organizations().table, Careers().table], 
                                ref_columns=[('city', 'name'), ('organization', 'name'), ('careers', 'name')], 
                                json=json,
                                connection_tables=[Careers_per_offer().table])
        
    def select_column(self, column_name, limit=None):
        return select_column(self.table, self.table_name, column_name, limit)
    
    def filter_htmls(self, htmls, codes):
        """
        Filter job offers htmls whose offer_page_code value are not in the database.
        """
        codes_database = self.select_column('offer_page_code')
        codes_database = [id[0] for id in codes_database]
        htmls_filtered = [html for code, html in zip(codes, htmls) if code not in codes_database]

        main_logger.info(f"Job offers htmls where filtered to {len(htmls_filtered)} htmls. Remaining job offers already registered in the database.")
        return htmls_filtered