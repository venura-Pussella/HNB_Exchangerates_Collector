import requests
from src import logger

def fetch_url_content(url):
    
    logger.info(">>>>>> Fetching HTML content from the URL <<<<<<")

    response = requests.get(url)
    response.raise_for_status()

    logger.info(">>>>>> Fetched HTML content successfully <<<<<<")
    return response.text
    
