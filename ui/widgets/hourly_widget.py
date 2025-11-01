from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class HourlyWidget(QFrame):
    def __init__(self, time_text="--", icon_text="☀️", temp_text="--°"):
        super().__init__()
        self.setFixedSize(100, 120)
        self.setStyleSheet("background: rgba(255,255,255,0.02); border-radius: 10px;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6,6,6,6)
        self.time_label = QLabel(time_text)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.icon_label = QLabel(icon_text)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.temp_label = QLabel(temp_text)
        self.temp_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.time_label)
        layout.addWidget(self.icon_label)
        layout.addWidget(self.temp_label)
