import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    MAPBOX_ACCESS_TOKEN = os.getenv('MAPBOX_ACCESS_TOKEN')
    DJANGO_SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')