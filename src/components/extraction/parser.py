import requests
import sys
from bs4 import BeautifulSoup

from src.exception import CustomException
from src.logger import logger


def get_soup(url):
    '''
    Gets the html of a web page and parses it. Returns soup object
    '''
    try:
        response = requests.get(url)
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')
        
        logger.info("HTML from URL parsed successfully")
        
        return soup
    
    except Exception as e:
        logger.error(f"Error getting parsed html: {e}.")
        raise CustomException(e, sys)