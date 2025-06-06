from src.components.extraction.extract import Extractor
from src.components.transformation.nlp_processing import Processor

from src.models.offers import Offers

def main():

    # 1. Extract hmtls and codes for all job offers
    extractor = Extractor("https://www.convocatoriasdetrabajo.com/convocatorias-practicas-profesionales-preprofesionales-vigentes.php")
    htmls, codes = extractor.extract_offers_htmls()

    # 2. Filter codes that are not in the database
    offers = Offers()
    htmls_filtered = offers.filter_htmls(htmls, codes)

    # 3. Process html and get the json
    processor = Processor(htmls_filtered)
    offer_details = processor.get_job_details()

    # 4. Insert data
    failed_offers = offers.insert_rows_dinamically(offer_details)

if __name__ == '__main__':
    main()
