import json
from typing import List, Dict, Union


def split_list(list_: list, n: int=12) -> List[List]:
    '''
    Splits a list into a list of lists of lenght n.
    '''

    n_values = len(list_)
    lists = [] # list of lists

    # Decides if the number of lists should be one or more
    if n < n_values:
        
        # Number of lists to split
        partitions = ((n_values // n) + 1) if (n_values % n) != 0 else (n_values//n)

        # Perform the creation of lists and appends to a main list
        for i in range(partitions):
            lists.append(list_[n*i:n*(i+1)])

    else:
        lists.append(list_)
    
    return lists


def write_to_file(data: list, filename: str):
        '''
        Writes data to a json file.
        '''
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data, ensure_ascii=False))


def read_to_json(filepath: str) -> Union[List[Dict], Dict]:
    '''
    Reads text JSON formatted to a JSON python object.
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