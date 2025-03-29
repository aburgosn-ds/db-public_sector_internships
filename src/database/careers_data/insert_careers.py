'''
Inserts all careers to the careers table.
'''

from src.utils.general_utils import read_to_json, get_careers
from src.constants.careers_data_constants import CAREERS_PATH
from src.models.careers import Careers


def main():
    json = read_to_json(CAREERS_PATH)
    careers_list = list(set(get_careers(json)))
    careers_json = [{'name': career} for career in careers_list]

    careers_obj = Careers()
    careers_obj.insert_rows(careers_json, one_by_one=False, get_pk=False)

if __name__ == '__main__':
    main()