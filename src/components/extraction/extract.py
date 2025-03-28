import sys
import asyncio
import aiohttp
import re

from typing import List, Dict
from bs4 import BeautifulSoup
from src.components.extraction.parser import get_soup

from src.logger import main_logger
from src.exception import CustomException


# Changes the asyncronous execution policy for Windows 
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class Extractor:

    def __init__(self, url):

        main_logger.info("Initializing Extractor class...")

        self.url = url
        self.soup = get_soup(url)
        self.offers_overview = []
        self.offers_htmls = {}

        main_logger.info("Extractor class initialized successfully.")


    def extract_offers_overview(self):
        """
        Get job offers information from the overview page, including the URL which contains a detailed description.
        """
        main_logger.info("Extracting offers overview information...")

        try:
            # List of job offer tags    
            offers_tag = self.soup.find_all('article', attrs={'class': 'convocatoria'})
        
            # Get some initial information for each job offer and store them into offers_overview 
            for offer_tag in offers_tag:

                try:
                    # entity = offer_tag.h4.text
                    # end_date = offer_tag.div.find('i', {"class": 'icon-calendario'}).find_next_sibling().text
                    city = offer_tag.div.find('i', {"class": 'icon-mapa1'}).find_next_sibling().text
                    url_offer = offer_tag.div.a['href']
                    offer_code = self._extract_offer_code(url_offer)        

                    offer = {
                        'offer_page_code': int(offer_code),
                        'city': city,
                        'url': url_offer
                    }

                    # self.offers_codes.append(int(offer_code))
                    self.offers_overview.append(offer)

                except AttributeError as e:
                    main_logger.warning(f"Error extracting an offer, skipping it: {e} ")

            main_logger.info("Offers overview extraction DONE.")

        except Exception as e:
            main_logger.error("Unexpected error while extracting offers overview: ", exc_info=True)
            raise CustomException(e, sys)
    
        return self.offers_overview
         
        
    def get_offers_url(self) -> List[str]:
        '''
        Get urls of all offers.
        '''
        if not self.offers_overview:
            self.extract_offers_overview()

        urls = [offer['url'] for offer in self.offers_overview]
        return urls
    

    async def __get_offer_html(self, session, offer_initial: dict) -> dict:
        """
        Asynchronously gets html of the whole description from an offer 
        as a dict with key: offer_page_code and value: html
        """
        url = offer_initial['url']

        try:
            # Makes a GET request asyncronously
            async with session.get(url) as response:
                content = await response.text() # Waits and get the page content, then reads it
                soup = BeautifulSoup(content, 'html.parser')
                
                html_1 = soup.find('h1').text
                html_2 = soup.find('article', attrs={'class': 'oferta'}).text

                if not html_1 or not html_2:
                    main_logger.warning(f"Missing elements in offer {url}, skipping.", exc_info=True)
                    return {}
        
                html = html_1 + html_2 + "\nEND OF HTML\n" + str(offer_initial)
                return {offer_initial['offer_page_code']: html}
            
        except Exception as e:
            main_logger.warning(f"Error extracting offer html from {url}, skipping.", exc_info=True)
            return {}
    

    async def __async_tasks_offer_html(self, session, offers_initial:List[Dict]) -> List[str]:
        """
        Creates asynchronous tasks to get html descriptions for all offers.
        """
        htmls = dict()

        # Create all tasks to be executed within the same context session
        tasks = [asyncio.create_task(self.__get_offer_html(session, offer_initial)) for offer_initial in offers_initial]

        for task in asyncio.as_completed(tasks):
            html = await task
            htmls.update(html)  
            
        return htmls
    

    async def __session_get_offers_htmls(self):
        '''
        Executes the asyncronous tasks for extraction of html descriptions for all offers.
        '''
        # Run within a client session
        if not self.offers_overview:
            self.extract_offers_overview()

        async with aiohttp.ClientSession() as session:
            result = await self.__async_tasks_offer_html(session, self.offers_overview)
            return result        
        

    def extract_offers_htmls(self) -> tuple[list, list]:
        '''
        Execute asynchronous methods and gets all offers htmls, returns together with its corresponding page codes.
        '''
        main_logger.info("Extracting offers htmls...")
        self.offers_htmls = asyncio.run(self.__session_get_offers_htmls())
        main_logger.info("Offers htmls extraction DONE.")

        htmls = list(self.offers_htmls.values())
        codes = list(self.offers_htmls.keys())

        return htmls, codes
    

    @staticmethod
    def _extract_offer_code(url: str) -> str:
        '''
        Extracts the offer code from the URL using regex.
        '''
        match = re.search(r'-(\d+)\.html', url)
        if match:
            return match.group(1)
        
        raise ValueError(f"Invalid URL format for extracting offer code: {url}")