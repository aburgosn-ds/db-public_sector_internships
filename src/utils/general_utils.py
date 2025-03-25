import requests
import sys
import json
import pandas as pd
from bs4 import BeautifulSoup

from src.exception import CustomException
from src.logger import logger

from typing import List, Dict, Union


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


def split_list(list_:list, n:int=13) -> List[List]:
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