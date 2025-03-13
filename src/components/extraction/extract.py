import sys
import asyncio
import aiohttp
import re

from typing import List, Dict
from bs4 import BeautifulSoup
from src.components.extraction.parser import get_soup

from src.logger import logger
from src.exception import CustomException


# Changes the asyncronous execution policy for Windows 
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class Extractor:

    def __init__(self, url):
        self.url = url
        self.soup = get_soup(url)
        self.offers_overview = []
        self.offers_htmls = []


    def extract_offers_overview(self):
        """
        Get job offers information from the overview page, including the URL for a detailed description.
        """
        try:
            offers_tag = self.soup.find_all('article', attrs={'class': 'convocatoria'})
            for offer_tag in offers_tag:
                
                # entity = offer_tag.h4.text
                # end_date = offer_tag.div.find('i', {"class": 'icon-calendario'}).find_next_sibling().text
                city = offer_tag.div.find('i', {"class": 'icon-mapa1'}).find_next_sibling().text
                url_offer = offer_tag.div.a['href']
                offer_code = self._extract_offer_code(url_offer)        

                offer = {
                    'offer_id': offer_code,
                    'city': city,
                    'url': url_offer
                }
                
                self.offers_overview.append(offer)

        except AttributeError as e:
            raise(CustomException(e, sys))
        
        except Exception as e:
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
    

    async def __get_offer_html(self, session, offer_initial: dict) -> str:
        """
        Gets html of the whole description from an offer.
        """
        url = offer_initial['url']

        # Makes a GET request asyncronously
        async with session.get(url) as response:
            content = await response.text() # Waits and get the page content, then reads it
            soup = BeautifulSoup(content, 'html.parser')
            
            html_1 = soup.find('h1').text
            html_2 = soup.find('article', attrs={'class': 'oferta'}).text
            html = html_1 + html_2 + "\nEND OF HTML\n" + str(offer_initial)

            return html
    

    async def __get_offers_htmls(self, session, offers_initial:List[Dict]) -> List[str]:
        """
        Creates asyncronous tasks to get html descriptions for all offers.
        """
        htmls = []

        # Create all tasks to be executed within the same context session
        tasks = [asyncio.create_task(self.__get_offer_html(session, offer_initial)) for offer_initial in offers_initial]

        for task in asyncio.as_completed(tasks):
            html = await task
            htmls.append(html)  
            
        return htmls
    

    async def _get_offers_htmls(self):
        '''
        Executes the asyncronous tasks for extraction of html descriptions for all offers.
        '''
        # Run within a client session
        try:
            if not self.offers_overview:
                self.extract_offers_overview()

            async with aiohttp.ClientSession() as session:
                result = await self.__get_offers_htmls(session, self.offers_overview)
                return result
            
        except Exception as e:
            raise CustomException(e, sys)
        
        
    def extract_offers_htmls(self):
        '''
        Gets all offers htmls from asyncronous methos.
        '''
        self.offers_htmls = asyncio.run(self._get_offers_htmls())
        return self.offers_htmls
    

    @staticmethod
    def _extract_offer_code(url: str) -> str:
        '''
        Extracts the offer code from the URL using regex.
        '''
        match = re.search(r'-(\d+)\.html', url)
        if match:
            return match.group(1)
        
        raise ValueError(f"Invalid URL format for extracting offer code: {url}")