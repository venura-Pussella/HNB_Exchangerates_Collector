import os
from src import logger

def ensure_directory_exists(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            
    except Exception as e:
        logger.error(f"Error ensuring directory exists: {e}")
        raise
