import logging
import os
from dataclasses import dataclass
logging.basicConfig(level=logging.INFO)
from openai import OpenAI

@dataclass
class Options:
    model: str = "gpt-3.5-turbo"
    available_models_openai = ['gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo', 'gpt-4', 'gpt-3.5-turbo']
    temperature: float = 0.0
    OPENAI_API_KEY: str = None
    client: OpenAI = None

    def load_from_env(self):
        # check if the environment variable is set
        if 'OPENAI_API_KEY' in os.environ:
            self.OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
        else:
            logging.warning("OPENAI_API_KEY environment variable not set, you will not be able to use the OpenAI API.")
            # do you want to set the environment variable here?
            response = input("Do you want to set the OPENAI_API_KEY environment variable now? (y/n): ")
            if response.lower() == 'y':    
                key = input("Enter your OpenAI API key: ")
                os.environ['OPENAI_API_KEY'] = key
                self.OPENAI_API_KEY = key
            else:
                logging.warning("OPENAI_API_KEY environment variable not set.")
                

    def create_openai_client(self):
        if self.OPENAI_API_KEY:
            logging.info("Creating OpenAI client")
            from openai import OpenAI
            self.client = OpenAI(api_key=self.OPENAI_API_KEY)
        else:
            logging.error("OPENAI_API_KEY environment variable not set.")
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        
    def initialize(self):
        self.load_from_env()
        self.create_openai_client()