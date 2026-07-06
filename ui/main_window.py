from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QListWidget,
    QStackedWidget,
    QLabel,
    QVBoxLayout,
    QStatusBar,
)
from PySide6.QtCore import Qt

from ui.styles import *

from ui.pages.home_page import HomePage
from ui.pages.assistant_page import AssistantPage
from ui.pages.math_page import MathPage
from ui.pages.report_page import ReportPage
from ui.pages.document_page import DocumentPage
from ui.pages.settings_page import SettingsPage


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"{APP_NAME} v{VERSION}")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.build_ui()

    def build_ui(self):

        # ---------------- Central Widget ----------------
        central = QWidget()
        self.setCentralWidget(central)

        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ---------------- Header ----------------
        header = QLabel("🦉 ATHENA AI")
        header.setAlignment(Qt.AlignCenter)
        header.setFixedHeight(60)

        header.setStyleSheet(f"""
            background:{COLORS["primary"]};
            color:white;
            font-size:24px;
            font-weight:bold;
        """)

        root_layout.addWidget(header)

        # ---------------- Content ----------------
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar
        self.sidebar = QListWidget()

        self.sidebar.addItems([
            "🏠 Home",
            "💬 Assistant",
            "🧮 Mathematics",
            "📄 Reports",
            "📚 Documents",
            "⚙️ Settings"
        ])

        self.sidebar.setFixedWidth(220)

        self.sidebar.setStyleSheet(f"""
            QListWidget {{
                background:{COLORS["sidebar"]};
                border:none;
                font-size:16px;
                padding:8px;
            }}

            QListWidget::item {{
                height:45px;
            }}

            QListWidget::item:selected {{
                background:{COLORS["primary"]};
                color:white;
                border-radius:6px;
            }}
        """)

        # Pages
        self.pages = QStackedWidget()

        self.pages.addWidget(HomePage())
        self.pages.addWidget(AssistantPage())
        self.pages.addWidget(MathPage())
        self.pages.addWidget(ReportPage())
        self.pages.addWidget(DocumentPage())
        self.pages.addWidget(SettingsPage())

        content_layout.addWidget(self.sidebar)
        content_layout.addWidget(self.pages)

        root_layout.addLayout(content_layout)

        # ---------------- Status Bar ----------------
        status = QStatusBar()

        status.showMessage("Ready | Offline Mode")

        self.setStatusBar(status)

        # ---------------- Signals ----------------
        self.sidebar.currentRowChanged.connect(
            self.pages.setCurrentIndex
        )

        self.sidebar.setCurrentRow(0)

