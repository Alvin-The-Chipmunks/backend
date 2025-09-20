from dotenv import load_dotenv
from loguru import logger
import os
load_dotenv()


class AttomManager:
    def __init__(self):
        self.url = "URL"
        self.api_key = os.environ['API_KEY']
    
    def get_community_data(self, criteria: str):
        # TODO - call the attom community API and return results
        # implement logic to process/extract/transform the data
        # for a specific criteria point according to the schema that will 
        # work best for the heatmap on the frontend
        
        # perhaps this can be broken further into seperate functions
        pass