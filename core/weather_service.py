# core/weather_service.py
import requests
import time
from collections import defaultdict, Counter
from .config import API_KEY, BASE_URL, UNITS
from .models import CityWeather, HourlyForecast, DailyForecast

REQUEST_TIMEOUT = 10  # seconds

class WeatherService:
    @staticmethod
    def fetch_weather(city: str) -> CityWeather:
        """
        Fetches weather using OpenWeatherMap 5-day/3-hour forecast endpoint
        and maps it to the CityWeather dataclass expected by the UI.
        """
        if not API_KEY:
            raise ValueError("Missing API_KEY (check .env and core/config.py)")

        # Build request
        params = {
            "q": city,
            "appid": API_KEY,
            "units": UNITS,
        }

        try:
            r = requests.get(BASE_URL, params=params, timeout=REQUEST_TIMEOUT)
        except requests.RequestException as exc:
            raise ValueError(f"Network error fetching forecast: {exc}")

        # Parse JSON
        try:
            data = r.json()
        except ValueError:
            raise ValueError("Invalid JSON response from weather API")

        # Handle API-level errors
        # OpenWeatherMap sometimes returns {"cod":"401", "message":"..."} (cod as str)
        if r.status_code != 200:
            # try to extract message from payload
            msg = data.get("message") if isinstance(data, dict) else f"HTTP {r.status_code}"
            raise ValueError(f"Weather API error: {msg}")

        # Required fields check
        if "list" not in data or "city" not in data:
            raise ValueError("Unexpected API response structure (missing 'list' or 'city').")

        forecast_list = data.get("list", [])  # list of 3-hour entries
        city_info = data.get("city", {})
        city_name = city_info.get("name") or city

        # If forecast_list empty -> bail
        if not forecast_list:
            raise ValueError(f"No forecast data returned for '{city_name}'")

        # --- Current: pick the earliest timestamp >= now or simply first item ---
        now_ts = int(time.time())
        current_item = None
        for item in forecast_list:
            if item.get("dt", 0) >= now_ts:
                current_item = item
                break
        if current_item is None:
            current_item = forecast_list[0]

        current_temp = current_item.get("main", {}).get("temp", 0)
        current_icon = ""
        try:
            current_icon = current_item.get("weather", [{}])[0].get("icon", "")
        except Exception:
            current_icon = ""

        # --- Hourly: take the next 7 forecast entries (3-hour steps) starting from current_item index ---
        hourly = []
        start_index = 0
        for idx, item in enumerate(forecast_list):
            if item is current_item:
                start_index = idx
                break

        # Choose up to 7 items starting from start_index (these are 3-hourly points)
        for h in forecast_list[start_index:start_index + 7]:
            ts = h.get("dt", int(time.time()))
            hourly.append(HourlyForecast(
                time=time.strftime("%I %p", time.localtime(ts)),
                temperature=h.get("main", {}).get("temp", 0),
                icon=h.get("weather", [{}])[0].get("icon", "")
            ))

        # --- Daily: aggregate per date (YYYY-MM-DD) across forecast_list ---
        daily_map = defaultdict(lambda: {"max": -9999, "min": 9999, "icons": []})
        for item in forecast_list:
            ts = item.get("dt", int(time.time()))
            day = time.strftime("%Y-%m-%d", time.localtime(ts))
            main = item.get("main", {})
            temp = main.get("temp", None)
            if temp is None:
                continue
            if temp > daily_map[day]["max"]:
                daily_map[day]["max"] = temp
            if temp < daily_map[day]["min"]:
                daily_map[day]["min"] = temp
            icon = item.get("weather", [{}])[0].get("icon", "")
            if icon:
                daily_map[day]["icons"].append(icon)

        # Convert daily_map to sorted list of DailyForecast (limit to next 7 days)
        days_sorted = sorted(daily_map.keys())
        daily = []
        for day_key in days_sorted[:7]:
            info = daily_map[day_key]
            # choose the most common icon in that day's entries (fallback to first)
            icon = None
            if info["icons"]:
                icon = Counter(info["icons"]).most_common(1)[0][0]
            else:
                icon = ""
            # convert 'YYYY-MM-DD' to weekday short label
            try:
                ts0 = int(time.mktime(time.strptime(day_key, "%Y-%m-%d")))
                day_label = time.strftime("%a", time.localtime(ts0))
            except Exception:
                day_label = day_key
            daily.append(DailyForecast(
                day=day_label,
                temp_max=info["max"] if info["max"] != -9999 else 0,
                temp_min=info["min"] if info["min"] != 9999 else 0,
                icon=icon
            ))

        # Compose CityWeather model and return
        return CityWeather(
            city=city_name,
            current_temp=current_temp,
            rain_chance=0,   # forecast endpoint provides 'pop' in each list item; you can compute if desired
            icon=current_icon,
            hourly=hourly,
            daily=daily
        )
