import os
import logging
from dotenv import load_dotenv

def load_env_variables():
    load_dotenv()
    return {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY'),
        'GOOGLE_SEARCH_ENGINE_ID': os.getenv('GOOGLE_SEARCH_ENGINE_ID'),
        'SMTP_HOST': os.getenv('SMTP_HOST'),
        'SMTP_FROM': os.getenv('SMTP_FROM'),
        'SMTP_FROM_NAME': os.getenv('SMTP_FROM_NAME'),
        'SMTP_PORT': int(os.getenv('SMTP_PORT')),
        'SMTP_USERNAME': os.getenv('SMTP_USERNAME'),
        'SMTP_PASSWORD': os.getenv('SMTP_PASSWORD'),
        'SMTP_SECURITY': os.getenv('SMTP_SECURITY'),
        'SMTP_AUTH_MECHANISM': os.getenv('SMTP_AUTH_MECHANISM'),
        'PLEX_AUTH_TOKEN': os.getenv('PLEX_AUTH_TOKEN'),
        'PLEX_USER_ID': os.getenv('PLEX_USER_ID')
    }

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='logs/app.log',
        filemode='a'
    )
    return logging.getLogger(__name__)

