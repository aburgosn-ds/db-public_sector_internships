
import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from google.generativeai.generative_models import GenerativeModel

import os
from dotenv import load_dotenv
import json
import asyncio
from src.utils import split_list, write_to_file
from dataclasses import dataclass
from src.components.transformation.utils.constants import SYS_INSTRUCTIONS

load_dotenv()
genai.configure(api_key=os.environ['API_KEY'])


@dataclass
class ProcessorConfig:
    response_mime_type: str = 'application/json'
    temperature: float = 0.2


class ProcessorModel:
    def __init__(self, config: ProcessorConfig):
        self.model = GenerativeModel(
            model_name = "gemini-2.0-flash-lite",
            generation_config = GenerationConfig(
                response_mime_type=config.response_mime_type,
                temperature=config.temperature
                ),
            system_instruction = SYS_INSTRUCTIONS
        )

class Processor:
    '''
    Asyncronous for handling job offers details
    '''
    def __init__(self, offers_html: list[str]):
        self.offers_html = offers_html
        self.config_model = ProcessorConfig()
        self.processor_model = ProcessorModel(self.config_model)


    async def get_async_job_details(self, save: bool = True):
        return await self._get_job_details_all(self.offers_html, save)
    

    async def _get_job_details_batch(self, input: list[str]):
        '''
        Gets the job offer details for a batch of offers
        '''
        response = await self.processor_model.model.generate_content_async(contents=input)

        json_ = json.loads(response.text)

        return json_


    async def _get_job_details_all(self, input: list[str], save: bool):
        '''
        Gets all job offers details for all batches.
        '''
        tasks = [asyncio.create_task(self._get_job_details_batch(input_)) for input_ in split_list(input)]
        jsons = []

        for task in asyncio.as_completed(tasks):
            json_ = await task
            jsons.extend(json_)      

        if save:
            write_to_file(jsons, 'temp.json')

        return jsons