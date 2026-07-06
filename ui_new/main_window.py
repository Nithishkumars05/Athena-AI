from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStackedWidget
)

from ui_new.widgets.sidebar import Sidebar
from ui_new.pages.dashboard import DashboardPage
from ui_new.pages.chat import ChatPage

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Athena AI v6")

        self.resize(1300, 800)

        central = QWidget()

        self.setCentralWidget(central)

        layout = QHBoxLayout(central)

        # Sidebar
        self.sidebar = Sidebar()
        layout.addWidget(self.sidebar)

        # Pages
        self.pages = QStackedWidget()

        self.dashboard = DashboardPage()
        self.pages.addWidget(self.dashboard)
        self.chat = ChatPage()
        self.pages.addWidget(self.chat)
        

        layout.addWidget(self.pages)

        self.sidebar.page_changed.connect(
            self.pages.setCurrentIndex
        )