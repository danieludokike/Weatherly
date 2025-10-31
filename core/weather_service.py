
import requests
import time
from .config import API_KEY, BASE_URL, GEOCODE_URL, UNITS
from .models import CityWeather, HourlyForecast, DailyForecast

class WeatherService:
    @staticmethod
    def fetch_weather(city: str) -> CityWeather:
        # Step 1: Get coordinates
        g = requests.get(GEOCODE_URL, params={"q": city, "limit": 1, "appid": API_KEY}).json()
        if not g:
            raise ValueError("City not found")
        lat, lon = g[0]["lat"], g[0]["lon"]

        # Step 2: Fetch weather data
        params = {"lat": lat, "lon": lon, "units": UNITS, "exclude": "minutely,alerts", "appid": API_KEY}
        data = requests.get(BASE_URL, params=params).json()

        # Step 3: Parse
        city_name = g[0]["name"]
        current = data["current"]
        rain_chance = int(data["daily"][0].get("pop", 0) * 100)
        icon = data["current"]["weather"][0]["icon"]

        hourly = []
        for h in data["hourly"][:7]:
            hourly.append(HourlyForecast(
                time=time.strftime("%I %p", time.localtime(h["dt"])),
                temperature=h["temp"],
                icon=h["weather"][0]["icon"]
            ))

        daily = []
        for d in data["daily"][:7]:
            daily.append(DailyForecast(
                day=time.strftime("%a", time.localtime(d["dt"])),
                temp_max=d["temp"]["max"],
                temp_min=d["temp"]["min"],
                icon=d["weather"][0]["icon"]
            ))

        return CityWeather(
            city=city_name,
            current_temp=current["temp"],
            rain_chance=rain_chance,
            icon=icon,
            hourly=hourly,
            daily=daily
        )
