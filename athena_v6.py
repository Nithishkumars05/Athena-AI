import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont

from ui_new.style import QSS
from ui_new.main_window import MainWindow
from core.logger import logger

def main():
    app = QApplication(sys.argv)

    app.setStyleSheet(QSS)
    app.setFont(QFont("Segoe UI", 10))
    logger.info("Athena started")
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()