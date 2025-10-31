
import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Applying global stylesheet
    try:
        with open("ui/styles/dark_theme.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("dark_theme.qss not found, running with default style.")

    # Launch main window
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


