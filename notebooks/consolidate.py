import pandas as pd


# Load tables data as dataframes
offers = pd.read_csv('offers.csv')
cities = pd.read_csv('cities.csv')
organizations = pd.read_csv('organizations.csv')
careers = pd.read_csv('careers.csv')
careers_per_offer = pd.read_csv('careers_per_offer.csv')

# Join careers with careers_per_offer and hen process
careers_per_offer_careers = pd.merge(careers_per_offer, careers, how='left', left_on='career_id', right_on='id', validate='many_to_one')
careers_per_offer_careers = pd.concat([careers_per_offer_careers.groupby('offer_id')['name'].agg(list), careers_per_offer_careers.groupby('offer_id')['career_id'].agg(list)], axis=1).reset_index()
careers_per_offer_careers.rename({'name': 'careers', 'career_id': 'careers_id'}, inplace=True, axis=1)

# Join previous df with offers and then process
offers_careers = pd.merge(offers, careers_per_offer_careers, how='right', left_on='id', right_on='offer_id', validate='one_to_many')
offers_careers.drop(columns='id', inplace=True)

# Join previous df with cities and then process
offers_careers_cities = pd.merge(offers_careers, cities, how='left', left_on='city_id', right_on='id', validate='many_to_one', suffixes=['', '_x'])
offers_careers_cities.drop(columns=['current_date_x', 'id'], inplace=True)
offers_careers_cities.rename({'name': 'city'}, inplace=True, axis=1)

# Join previous df with organizations and then process
offers_careers_cities_organizations = pd.merge(offers_careers_cities, organizations, how='left', left_on='organization_id', right_on='id', validate='many_to_one', suffixes=['', '_x'])
offers_careers_cities_organizations.drop(columns=['current_date_x', 'id'], inplace=True)
offers_careers_cities_organizations.rename({'name': 'organization'}, inplace=True, axis=1)


# Save consolidate offers data
offers_careers_cities_organizations.to_csv('consolidate.csv', index=False)