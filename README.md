
# Weatherly — Modern Python Weather App (PySide6)

**Weatherly** is a modern, elegant desktop weather application built with **Python** and **PySide6 (Qt for Python)**.  
It fetches real-time weather and forecast data using the **OpenWeatherMap API**, automatically detects your current location, and provides a sleek, responsive UI that feels professional and fast.

<img width="829" height="502" alt="img" src="https://github.com/user-attachments/assets/20c48b01-291f-480f-b9df-fc2e37c22cc8" />

## Features

1. **Automatic Location Detection**  
Weatherly detects your current city via IP-based geolocation and instantly loads your local weather on startup.

2. **Search Any City**  
Type a city name and hit **Enter** or **Search** to see its real-time temperature, weather icon, and 5-day forecast.

3. **Live Data from OpenWeatherMap**  
Weatherly uses the **free `/data/2.5/forecast` API** from [OpenWeatherMap](https://openweathermap.org/api) to display:
- Current temperature
- Hourly forecast (next few hours)
- 7-day forecast with daily highs and lows
- Basic air condition details (rain chance, wind, UV, etc.)

4. **Beautiful UI Built with PySide6**  
- Minimal, clean design using Qt widgets and layouts  
- Styled with custom QSS themes  
- Sidebar icons for easy navigation  
- Responsive layout for large and small screens

5. **Async Weather Fetching with Preloader**  
All data requests run in background threads — the UI never freezes.  
The **Search** button changes to **“Loading…”** while data is being fetched.

6. **Modular Project Structure**  
Organized into `core` and `ui` layers for clean separation of logic, services, and presentation.


## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/danieludokike/Weatherly.git
cd Weatherly
2. Create a Virtual Environment
python -m venv env
source env/bin/activate    # (Linux/macOS)
env\Scripts\activate       # (Windows)
3. Install Dependencies
pip install -r requirements.txt

API_KEY=your_openweathermap_api_key
UNITS=metric

You can get your free API key from:
https://home.openweathermap.org/api_keys

Make sure your key is active and you’re using the free forecast API endpoint:


https://api.openweathermap.org/data/2.5/forecast
▶️ Run the App
python main.py
You’ll see a window titled “Weatherly” open with:

Your current location’s weather (auto-detected)

Search bar to fetch other cities

5-day forecast and hourly summary

API Reference
Weatherly uses:

Forecast API: /data/2.5/forecast

Parameters:

q: city name

appid: your API key

units: metric or imperial

Geolocation API: http://ip-api.com/json

No key required (used to detect user’s city)

    Technical Highlights
Layer	Description
Core	Contains data logic, config, and weather service (API fetching).
UI	Handles presentation and user interaction.
Threading	Weather fetching runs in a background thread to avoid freezing the interface.
Styling	Custom Qt stylesheet (dark_theme.qss) for a clean, professional dark mode look.
Separation of Concerns	Logic, UI, and data models are all kept independent.


Contributions are welcome!
If you’d like to improve Weatherly:

Fork this repository

Create a new branch (git checkout -b feature-name)

Commit your changes (git commit -m "Added feature XYZ")

Push to your fork (git push origin feature-name)

Submit a Pull Request

License
This project is licensed under the MIT License — feel free to use, modify, and distribute.

Author
Udokike Daniel
Python Developer | Educator | Open Source Contributor
Nigeria
• https://github.com/danieludokike/Weatherly 
• https://www.linkedin.com/in/udokike-daniel-ba9148210 
