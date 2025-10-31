
from dataclasses import dataclass
from typing import List

@dataclass
class HourlyForecast:
    time: str
    temperature: float
    icon: str

@dataclass
class DailyForecast:
    day: str
    temp_max: float
    temp_min: float
    icon: str

@dataclass
class CityWeather:
    city: str
    current_temp: float
    rain_chance: int
    icon: str
    hourly: List[HourlyForecast]
    daily: List[DailyForecast]
