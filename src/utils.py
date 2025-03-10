import requests
import sys
from bs4 import BeautifulSoup
from src.exception import CustomException
import pandas as pd

def get_soup(url):
    '''
    Gets the html of a web page and parses it. Returns soup object
    '''
    try:
        response = requests.get(url)
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')
        
        return soup
    
    except Exception as e:
        raise CustomException(e, sys)


def get_careers_from_web():
    '''
    Gets all available careers from the same web as the internship offers portal
    '''
    # Gets the html parsed
    soup = get_soup("https://www.convocatoriasdetrabajo.com/carreras")

    try:
        columns = soup.find_all('div', attrs={'class': 'columnas3'})[1].find_all('div', attrs={'class': 'columna'})

        # Gets all careers from the page structure
        col1 = columns[0].find('div')
        ing_tec_cons = [tag.text for tag in col1.find_all('a')]
        col2 = columns[1].find('div')
        cie_mark_fin_otr = [tag.text for tag in col2.find_all('a')]

        careers = ing_tec_cons + cie_mark_fin_otr

        return careers

    except Exception as e:
        raise CustomException(e, sys)
    

def get_organizations_list():
    '''
    Gets all available organizations who offers the internships from the same web as the internship offers portal
    '''
    # Gets the html parsed
    soup = get_soup("https://www.convocatoriasdetrabajo.com/organizaciones")

    try:
        org_boxes = soup.find_all('div', attrs={'class': 'card card--min'})
        # Gets all organization from the page structure
        organizations = []

        for org_box in org_boxes:
            organization = org_box.find('h2').text
            organizations.append(organization)
    
        return organizations

    except Exception as e:
        raise CustomException(e, sys)
    

def get_careers_from_official():
    '''
    Gets all professional programs available in all universities in Peru
    Source SUNEDU: https://metraslado.pe/carreras
    '''
    df = pd.read_excel('data/data_tables/professional_programs_raw.xlsx', sheet_name='Hoja 1', header=4, usecols=[2,3])
    df.dropna(inplace=True)
    careers = df['Programa'].unique().tolist()

    with open('data/data_tables/professional_programs_raw.txt', 'w', encoding='utf-8') as file:
        file.write('career\n')

        for career in careers:
            file.write(career+'\n')

    return careers


def change_key_value(dict_:dict, key_value:dict, new_key_value:dict):
    '''
    This function changes a key-value pair from a dict to anoter key-value
    in the same position
    '''

    key = list(key_value.keys())[0]
    new_key = list(new_key_value.keys())[0]

    new_keys = list(dict_.keys()).copy()
    new_keys[new_keys.index(key)] = new_key

    value = list(key_value.values())[0]
    new_value = list(new_key_value.values())[0]

    new_values = list(dict_.values()).copy()
    new_values[new_values.index(value)] = new_value

    new_dict_ = {key: value for key,value in zip(new_keys, new_values)}

    return new_dict_

a = {'a': 1, 'b': 2}

print(change_key_value(a, {'a': 1}, {'hola': 20}))
