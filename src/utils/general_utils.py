import requests
import sys
from bs4 import BeautifulSoup
from src.exception import CustomException
import pandas as pd
from typing import List, Dict, Union
import json

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

    new_keys = list(dict_.keys()).copy() # List of old keys
    new_keys[new_keys.index(key)] = new_key # Changes the old key with the new key

    value = list(key_value.values())[0]
    new_value = list(new_key_value.values())[0]

    new_values = list(dict_.values()).copy() # List of old values
    new_values[new_values.index(value)] = new_value # Changes the old value with the new value

    # Joins new keys and new values into a dictionary
    new_dict_ = {key: value for key,value in zip(new_keys, new_values)}

    return new_dict_


def split_list(list_:list, n:int=10) -> List[List]:
    '''
    This function splits a list into lists of lenght n
    '''

    n_values = len(list_)
    lists = []

    if n < n_values:
        
        partitions = ((n_values // n) + 1) if (n_values % n) != 0 else (n_values//n)

        for i in range(partitions):
            lists.append(list_[n*i:n*(i+1)])

    else:
        lists.append(list_)
    
    return lists


def filter_key_value(json:List[Dict], include_keys:List):
    '''
    This function filters key-value pairs for each dictionary in a list of dictionaries
    '''
    filtered_json = []

    for dict_ in json:
        temp_dict = dict_.copy()
        for key in dict_:
            if key not in include_keys:
                temp_dict.pop(key)
        filtered_json.append(temp_dict)

    return filtered_json

def multiply_dicts(json: List[Dict]):
    new_json = []
    for dict_ in json:
        new_dicts = [{'offer_id': dict_['offer_id'], 'career_id': career_id} for career_id in dict_['career_id']]
        new_json.extend(new_dicts)

    return new_json


def write_to_file(data: list, filename: str):
        '''
        Writes data to a json file.
        '''
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data, ensure_ascii=False))


def read_to_json(filepath: str) -> Union[List[Dict], Dict]:
    '''
    Reads text JSON formatted to a JSON python objett
    '''
    with open(filepath, 'r', encoding='utf-8') as file:
        text = file.read()
        return json.loads(text)
    


def get_careers(dict_careers):
    '''
    Extract a list of all careers.
    '''
    careers = []

    for education_field in dict_careers:
        specific_fields = dict_careers[education_field]
        for specific_field in specific_fields:
            detail_fields = specific_fields[specific_field]
            for detail_field in detail_fields:
                careers_inside = detail_fields[detail_field]
                careers.extend(careers_inside)

    return clean_careers(careers)



def clean_careers(careers, sort=True):
    '''
    Cleans the added slash (/) for some careers and sort the list.
    '''
    careers_cleaned = []
    for career in careers:
        if "/" in career:
            careers_cleaned.append(career[:-3])
        else:
            careers_cleaned.append(career)

    if sort:
        careers_cleaned.sort()

    return careers_cleaned