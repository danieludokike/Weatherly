
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class HourlyWidget(QFrame):
    def __init__(self, time_text="--", icon_text="☀️", temp_text="--°"):
        super().__init__()
        self.setFixedSize(100, 120)
        self.setStyleSheet("background: rgba(255,255,255,0.05); border-radius: 10px;")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(time_text, alignment=Qt.AlignCenter))
        layout.addWidget(QLabel(icon_text, alignment=Qt.AlignCenter))
        layout.addWidget(QLabel(temp_text, alignment=Qt.AlignCenter))
