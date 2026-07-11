from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStackedWidget,
    QLabel
)
from PySide6.QtCore import Qt,QTimer

from ui_new.widgets.sidebar import Sidebar

from ui_new.pages.dashboard import DashboardPage
from ui_new.pages.chat import ChatPage
from ui_new.pages.chat import ChatPage
from ui_new.pages.math import MathPage
from ui_new.pages.reports import ReportsPage
from ui_new.pages.documents import DocumentsPage
from ui_new.pages.projects import ProjectsPage
from ui_new.pages.settings import SettingsPage


class PlaceholderPage(QWidget):

    def __init__(self, title):
        super().__init__()

        layout = QHBoxLayout(self)

        label = QLabel(f"{title}\n\nComing Soon...")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            font-size:28px;
            color:#999999;
        """)

        layout.addWidget(label)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Athena AI v6")
        self.resize(1300, 800)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)

        # ==========================
        # Sidebar
        # ==========================
        self.sidebar = Sidebar()
        layout.addWidget(self.sidebar)

        # ==========================
        # Pages
        # ==========================
        self.pages = QStackedWidget()

        self.dashboard = DashboardPage()
        self.chat = ChatPage()

        self.math = MathPage()
        self.reports = ReportsPage()
        self.documents = DocumentsPage()
        self.projects = ProjectsPage()

        self.settings = SettingsPage()

        self.pages.addWidget(self.dashboard)     # 0
        self.pages.addWidget(self.chat)          # 1
        self.pages.addWidget(self.math)          # 2
        self.pages.addWidget(self.reports)       # 3
        self.pages.addWidget(self.documents)     # 4
        self.pages.addWidget(self.projects)      # 5
        self.pages.addWidget(self.settings)      # 6

        layout.addWidget(self.pages)

        # ==========================
        # Navigation
        # ==========================
        self.sidebar.page_changed.connect(
            self.pages.setCurrentIndex
        )

    def showEvent(self, event):
        super().showEvent(event)

        QTimer.singleShot(
        250,
        lambda: self.chat.chat.input_box.setFocus()
    )