import pandas as pd
from src.database.db_connection import get_connection

def main():
    engine = get_connection()

    # Load database tables as dataframes
    offers = pd.read_sql_table('offers', con=engine)
    cities = pd.read_sql_table('cities', con=engine)
    organizations = pd.read_sql_table('organizations', con=engine)
    careers = pd.read_sql_table('careers', con=engine)
    careers_per_offer = pd.read_sql_table('careers_per_offer', con=engine)

    # Save data to csv
    offers.to_csv('offers.csv', index=False)
    cities.to_csv('cities.csv', index=False)
    organizations.to_csv('organizations.csv', index=False)
    careers.to_csv('careers.csv', index=False)
    careers_per_offer.to_csv('careers_per_offer.csv', index=False)

if __name__ == '__main__':
    main()
