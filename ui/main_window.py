
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel,
    QListWidget, QListWidgetItem, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, QThread, Signal, QSize
from core.weather_service import WeatherService
from ui.widgets.hourly_widget import HourlyWidget


class FetchWeatherThread(QThread):
    result = Signal(object)
    error = Signal(str)

    def __init__(self, city):
        super().__init__()
        self.city = city

    def run(self):
        try:
            data = WeatherService.fetch_weather(self.city)
            self.result.emit(data)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weatherly")
        self.setMinimumSize(1100, 650)
        self.thread = None
        self._build_ui()

        try:
            from core.location_service import LocationService
            city, _, _ = LocationService.get_current_city()
            self._fetch_weather(city)
        except Exception as e:
            print("Startup fetch error:", e)

    # ---------------------- UI Layout ----------------------
    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(14)

        # Left Sidebar
        sidebar = QFrame()
        sidebar.setObjectName("leftSidebar")
        sidebar.setFixedWidth(88)
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(10, 10, 10, 10)
        sb_layout.setSpacing(12)
        for glyph in ["🌬", "📍", "🗺", "⚙️"]:
            btn = QPushButton(glyph)
            btn.setFixedSize(56, 56)
            btn.setObjectName("sidebarButton")
            btn.setFlat(True)
            sb_layout.addWidget(btn, alignment=Qt.AlignTop)
        sb_layout.addStretch()
        root.addWidget(sidebar)

        # Center Column
        center_container = QVBoxLayout()
        center_container.setSpacing(12)

        # Search Row
        top_row = QHBoxLayout()
        self.search = QLineEdit(placeholderText="Search for cities")
        self.search.setFixedHeight(40)
        self.search.returnPressed.connect(self._on_search)
        self.search.setObjectName("searchInput")
        self.search_button = QPushButton("Search", clicked=self._on_search)
        self.search_button.setFixedHeight(40)
        top_row.addWidget(self.search)
        top_row.addWidget(self.search_button)
        center_container.addLayout(top_row)

        # Big Card
        big_card = QFrame()
        big_card.setObjectName("bigCard")
        big_card.setMinimumHeight(180)
        big_layout = QHBoxLayout(big_card)
        big_layout.setContentsMargins(18, 16, 18, 16)
        left_info = QVBoxLayout()
        self.city_lbl = QLabel("City")
        self.city_lbl.setObjectName("cityLabel")
        self.chance_lbl = QLabel("Chance of rain: --")
        self.temp_lbl = QLabel("--°")
        self.temp_lbl.setObjectName("bigTemp")
        left_info.addWidget(self.city_lbl)
        left_info.addWidget(self.chance_lbl)
        left_info.addStretch()
        left_info.addWidget(self.temp_lbl)
        big_layout.addLayout(left_info, stretch=2)
        self.icon_lbl = QLabel("☀️")
        self.icon_lbl.setObjectName("bigIcon")
        self.icon_lbl.setFixedSize(140, 140)
        self.icon_lbl.setAlignment(Qt.AlignCenter)
        big_layout.addWidget(self.icon_lbl, alignment=Qt.AlignRight)
        center_container.addWidget(big_card)

        # Hourly Card
        hourly_card = QFrame()
        hourly_card.setObjectName("hourlyCard")
        hourly_layout = QHBoxLayout(hourly_card)
        hourly_layout.setContentsMargins(12, 12, 12, 12)
        hourly_layout.setSpacing(10)
        self.hourly_widgets = []
        for _ in range(7):
            w = HourlyWidget("--", "☀️", "--°")
            hourly_layout.addWidget(w)
            self.hourly_widgets.append(w)
        center_container.addWidget(hourly_card)

        # Air Card
        air_card = QFrame()
        air_card.setObjectName("airCard")
        air_layout = QHBoxLayout(air_card)
        left_vals = QVBoxLayout()
        self.real_feel_lbl = QLabel("Real Feel: --°")
        self.rain_chance_lbl = QLabel("Chance of rain: --%")
        left_vals.addWidget(QLabel("Air Conditions"))
        left_vals.addWidget(self.real_feel_lbl)
        left_vals.addWidget(self.rain_chance_lbl)
        air_layout.addLayout(left_vals)
        air_layout.addStretch()
        right_vals = QVBoxLayout()
        self.wind_lbl = QLabel("Wind: --")
        self.uv_lbl = QLabel("UV Index: --")
        right_vals.addWidget(self.wind_lbl)
        right_vals.addWidget(self.uv_lbl)
        air_layout.addLayout(right_vals)
        center_container.addWidget(air_card)
        root.addLayout(center_container, stretch=2)

        # Right Column
        right_col = QVBoxLayout()
        right_col.setSpacing(12)
        header = QLabel("7-DAY FORECAST")
        header.setObjectName("rightHeader")
        right_col.addWidget(header)
        self.daily_list = QListWidget()
        self.daily_list.setObjectName("dailyList")
        self.daily_list.setFixedWidth(320)
        right_col.addWidget(self.daily_list)
        right_col.addStretch()
        root.addLayout(right_col, stretch=1)

    # ---------------------- Logic ----------------------
    def _on_search(self):
        city = self.search.text().strip()
        if not city:
            return
        self._fetch_weather(city)

    def _fetch_weather(self, city):
        # Prevent multiple fetches
        if self.thread and self.thread.isRunning():
            print("Fetch already in progress — ignoring.")
            return

        # Disable input and show loading text
        self.search.setEnabled(False)
        self.search_button.setEnabled(False)
        self.search_button.setText("Loading...")
        self.search.setPlaceholderText("Fetching...")

        self.thread = FetchWeatherThread(city)
        self.thread.setParent(self)
        self.thread.result.connect(self._on_fetch_success)
        self.thread.error.connect(self._on_fetch_error)
        self.thread.finished.connect(self._on_fetch_finished)
        self.thread.start()

    def _on_fetch_success(self, data):
        try:
            self._update_ui(data)
        except Exception as e:
            QMessageBox.critical(self, "UI Error", f"Problem updating display:\n{e}")

    def _on_fetch_error(self, msg):
        print("Error fetching weather:", msg)
        QMessageBox.warning(self, "Weather Error", msg)

    def _on_fetch_finished(self):
        # Restore search button and input
        self.search.setEnabled(True)
        self.search_button.setEnabled(True)
        self.search_button.setText("Search")
        self.search.setPlaceholderText("Search for cities")

        if self.thread:
            self.thread.deleteLater()
            self.thread = None

    # ---------------------- Icon Helpers ----------------------
    def _map_icon(self, description_or_code):
        m = {
            "01d": "☀️", "01n": "🌙", "02d": "🌤", "03d": "⛅",
            "04d": "☁️", "09d": "🌧", "10d": "🌦", "11d": "⚡",
            "13d": "❄️", "50d": "🌫"
        }
        key = (description_or_code or "").lower()
        if description_or_code in m:
            return m[description_or_code]
        if "clear" in key:
            return "☀️"
        if "cloud" in key:
            return "☁️"
        if "rain" in key:
            return "🌧"
        if "storm" in key or "thunder" in key:
            return "⚡"
        if "snow" in key:
            return "❄️"
        return "🌤"

    def _update_ui(self, data):
        self.city_lbl.setText(data.city)
        self.temp_lbl.setText(f"{data.current_temp:.0f}°")
        self.chance_lbl.setText(f"Chance of rain: {data.rain_chance}%")
        self.icon_lbl.setText(self._map_icon(data.icon))

        for hw, h in zip(self.hourly_widgets, data.hourly):
            hw.time_label.setText(h.time)
            hw.icon_label.setText(self._map_icon(h.icon))
            hw.temp_label.setText(f"{h.temperature:.0f}°")

        self.daily_list.clear()
        for d in data.daily:
            item = QListWidgetItem()
            w = QLabel(f"{d.day}    {d.temp_max:.0f}/{d.temp_min:.0f}°    {self._map_icon(d.icon)}")
            w.setFixedHeight(42)
            item.setSizeHint(QSize(0, 42))
            self.daily_list.addItem(item)
            self.daily_list.setItemWidget(item, w)

    def closeEvent(self, event):
        """Ensure background threads close cleanly."""
        if self.thread and self.thread.isRunning():
            print("Waiting for worker to finish...")
            self.thread.quit()
            self.thread.wait(2000)
        super().closeEvent(event)
