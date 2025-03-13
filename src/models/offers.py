from src.database.load_db_metadata import load_metadata
from src.database.insert_data import insert_rows, insert_rows_dinamically
from src.database.select_data import select_column

from src.logger import logger
from src.exception import CustomException


metadata = load_metadata()
class Offers:

    def __init__(self):
        self.table_name = 'offers'
        self.table = metadata.tables[self.table_name]
        self.columns = self.table.columns.keys()

    def insert_rows(self, json):
        insert_rows(self.table_name, json)

    def insert_rows_dinamically(self, json):
        insert_rows_dinamically(self.table_name, 
                                columns=['specific_location_id', 'city_id', 'organization_id', 'career_id'], 
                                ref_tables_name=['specific_locations', 'cities', 'organizations', 'careers'], 
                                ref_columns=[('specific_location', 'address'), ('city', 'name'), ('organization', 'name'), ('careers', 'name')], 
                                json=json,
                                connection_tables='careers_per_offer')
        
    def select_column(self, column_name, limit=None):
        return select_column(self.table_name, column_name, limit)
    

if __name__=='__main__':
    a = Offers()
    json = [
        {'offer_page_code': '954482',
        'offer_title': 'Practicante de Psicología, Administración',
        'vacants': '01',
        'type': 'profesional',
        'to_apply': 'Egresado de la carrera universitaria en Psicología, Administración',
        'specifit_requirements': '',
        'knowledge': '',
        'salary': '1200.00',
        'responsabilities': '',
        'end_date': '2025-03-14',
        'url': 'https://www.convocatoriasdetrabajo.com/oportunidad-laboral-practicas-ministerio-economia-mef-psicologia-administracion-marzo-2025-467565.html',
        'specific_location': 'SEDE CENTRAL DEL MEF JR. JUNIN Nº 319 CERCADO DE LIMA LIMA LIMA',
        'city': 'CAXAMARCA',
        'organization': 'SUNAT',
        'careers': ['cico', 'sci', 'css'] }
        ]
    
    a.insert_rows_dinamically(json)