from typing import Dict, List
import re


def remove_ispace(string: str):
    '''
    Remove innecessary spaces.
    '''
    string = re.sub(r"\s+", " ", string)
    return string.strip()


def clean_dict(dict_: Dict):
    '''
    Cleans all strings for values in a dict offer.
    '''    
    # Iterates over all keys whose values are going to be cleaned
    for key in dict_:
        value = dict_[key] 

        # If there are/is value as data, process, otherwise do anything for that key:value pair
        if value:
            # If the value is a list, clean each element, otherwise (is a string) clean the value
            if type(value) == list:
                new_value = []
                # Cleans each list value
                for elm in value:
                    new_value.append(remove_ispace(elm))
                dict_[key] = new_value
            elif type(value) == str:
                dict_[key] = remove_ispace(value)
    return dict_


def clean_json(json: List[Dict]):
    '''
    Cleans all strings for all offers.
    '''
    cleaned_json = []

    for dict_ in json:
        cleaned_json.append(clean_dict(dict_))
    
    return cleaned_json


def uniform_strings(dict_: Dict):
    '''
    Converts lists values to string and set None if value is "".
    '''

    to_change = ["specific_requirements", "knowledge", "responsabilities"]

    for key in dict_:
        value = dict_[key]

        string = None
        if value:
            if key in to_change:
                string = "\n".join( elm for elm in value )
            
            else:
                string = value

        dict_[key] = string
    
    return dict_


def correct_format(json: List[Dict]):
    '''
    Changes list values to string for all offers.
    '''
    new_json = []
    
    for dict_ in json:
        new_json.append(uniform_strings(dict_))

    return new_json


def ready_to_insert(json: List[Dict]):
    '''
    Clean and correct json to insert the table.
    '''
    cleaned = clean_json(json)
    corrected = correct_format(cleaned)
    return corrected


def validate_offer_detail(offer_detail: Dict):
    '''
    Assess format for each value. Returns true if the offer has a validate format, or false otherwise.
    '''