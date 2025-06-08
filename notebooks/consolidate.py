import pandas as pd
from src.database.db_connection import get_connection

engine = get_connection()

# Load database tables as dataframes
offers = pd.read_sql_table('offers', con=engine)
cities = pd.read_sql_table('cities', con=engine)
organizations = pd.read_sql_table('organizations', con=engine)
careers = pd.read_sql_table('careers', con=engine)
careers_per_offer = pd.read_sql_table('careers_per_offer', con=engine)

# Join tables to get a consolidate table
careers_per_offer_careers = pd.merge(careers_per_offer, careers, how='left', left_on='career_id', right_on='id', validate='many_to_one', suffixes=['_a', '_b'])
offers_careers = pd.merge(offers, careers_per_offer_careers, how='right', left_on='id', right_on='offer_id', validate='one_to_many',  suffixes=['_c', '_d'])
offers_careers_cities = pd.merge(offers_careers, cities, how='left', left_on='city_id', right_on='id', validate='many_to_one', suffixes=['_e', '_f'])
offers_all = pd.merge(offers_careers_cities, organizations, how='left', left_on='organization_id', right_on='id', validate='many_to_one', suffixes=['_g', '_h'])

# Drop timestamps that came from all tables except that from offers table
offers_all.drop(columns=['current_date_a', 'current_date_b', 'current_date_f', 'current_date'], inplace=True)

# Drop primary keys, foreign keys have the same information
offers_all.drop(columns=['id_c', 'id_d', 'id_g', 'id_h'], inplace=True)

# Rename columns
offers_all.rename({'current_date_e': 'current_date', 'name': 'organization', 'name_e': 'career', 'name_f': 'city'}, inplace=True)


# Save table as csv
offers_all.to_csv("notebooks/offers_data.csv", index=False)