'''
Writes careers and their classifications from a PDF to a JSON file.
'''

from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import pathlib
import json
from src.utils.general_utils import write_to_file

from src.database.careers_data.constants import SYSTEM_INSTRUCTIONS, PROMPT_1, PROMPT_2, PDF_PTH


def main():
    
    # Load environment variables
    load_dotenv()

    try:
        client = genai.Client(api_key=os.environ['API_KEY'])

        # Read PDF as bytes
        filepath = pathlib.Path(PDF_PTH)
        file_bytes = filepath.read_bytes()

        result = dict() # 

        # Process the document as two parts due to the output token limit 
        for prompt in [PROMPT_1, PROMPT_2]:
            # Request the gemini model to extract information from PDF in JSON format
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    types.Part.from_bytes(
                        data=file_bytes,
                        mime_type='application/pdf'
                    ),
                    prompt
                ],
                config=types.GenerateContentConfig(
                    response_mime_type='application/json',
                    temperature = 0.2,
                    system_instruction=SYSTEM_INSTRUCTIONS
                )
            )

            # Load response as json and appends to the result dictionary
            as_json = json.loads(response.text)
            result.update(as_json)

        # Write result to a json file
        write_to_file(result, 'data/data_tables/careers.json')
    
    except Exception as e:
        print(str(e))
        raise Exception
    
if __name__ == '__main__':
    main()