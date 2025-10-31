
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt, QThread, Signal
from core.weather_service import WeatherService
from ui.widgets.hourly_widget import HourlyWidget

class FetchWeatherThread(QThread):
    result = Signal(object)
    error = Signal(str)
    def __init__(self, city): super().__init__(); self.city = city
    def run(self):
        try:
            data = WeatherService.fetch_weather(self.city)
            self.result.emit(data)
        except Exception as e:
            self.error.emit(str(e))

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.setMinimumSize(1100, 650)
        self._build_ui()
        self._fetch_weather("Madrid")

    def _build_ui(self):
        layout = QVBoxLayout(self)
        self.search = QLineEdit(placeholderText="Search for a city")
        self.button = QPushButton("Search", clicked=self._on_search)
        h = QHBoxLayout(); h.addWidget(self.search); h.addWidget(self.button)
        layout.addLayout(h)
        self.city_lbl = QLabel("City", alignment=Qt.AlignCenter)
        self.temp_lbl = QLabel("--°", alignment=Qt.AlignCenter)
        self.hourly_area = QHBoxLayout()
        layout.addWidget(self.city_lbl)
        layout.addWidget(self.temp_lbl)
        layout.addLayout(self.hourly_area)
        self.daily_list = QListWidget()
        layout.addWidget(self.daily_list)

    def _on_search(self):
        city = self.search.text().strip()
        if city: self._fetch_weather(city)

    def _fetch_weather(self, city):
        self.thread = FetchWeatherThread(city)
        self.thread.result.connect(self._update_ui)
        self.thread.error.connect(lambda e: print("Error:", e))
        self.thread.start()

    def _update_ui(self, data):
        self.city_lbl.setText(data.city)
        self.temp_lbl.setText(f"{data.current_temp:.0f}°")
        # Hourly
        for i in reversed(range(self.hourly_area.count())):
            self.hourly_area.itemAt(i).widget().deleteLater()
        for h in data.hourly:
            self.hourly_area.addWidget(HourlyWidget(h.time, "☀️", f"{h.temperature:.0f}°"))
        # Daily
        self.daily_list.clear()
        for d in data.daily:
            item = QListWidgetItem(f"{d.day} — {d.temp_max:.0f}/{d.temp_min:.0f}°")
            self.daily_list.addItem(item)
