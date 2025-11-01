
import os
from dotenv import load_dotenv

# Load and fetch environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"
GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct"
UNITS = os.getenv("UNITS", "metric")

if not API_KEY:
    raise ValueError("Missing API_KEY in .env")
