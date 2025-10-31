
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/onecall"
GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct"
UNITS = "metric"