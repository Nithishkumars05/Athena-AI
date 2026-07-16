from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

from app.branding import APP_NAME, TAGLINE


class Sidebar(QWidget):

    page_changed = Signal(int)

    def __init__(self):
        super().__init__()

        self.setObjectName("Sidebar")
        self.setFixedWidth(220)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(10)

        # --------------------------------
        # Branding
        # --------------------------------

        self.title = QLabel(f"✒ {APP_NAME}")
        self.title.setObjectName("Title")
        self.title.setAlignment(Qt.AlignCenter)

        self.subtitle = QLabel(TAGLINE)
        self.subtitle.setObjectName("Subtitle")
        self.subtitle.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.title)
        layout.addWidget(self.subtitle)
        layout.addSpacing(25)

        # --------------------------------
        # Navigation
        # --------------------------------

        self.buttons = []

        pages = [
            "🏠 Home",
            "💬 AI Chat",
            "🧮 Mathematics",
            "📄 Reports",
            "📚 Documents",
            "📁 Projects",
            "⚙ Settings",
        ]

        for index, page in enumerate(pages):

            button = QPushButton(page)
            button.setFixedHeight(42)
            button.setCursor(Qt.PointingHandCursor)
            button.setFocusPolicy(Qt.NoFocus)
            button.clicked.connect(
                lambda checked=False, i=index: self.change_page(i)
            )

            layout.addWidget(button)
            self.buttons.append(button)

        layout.addStretch()

        self.highlight(0)

    def change_page(self, index):

        self.highlight(index)
        self.page_changed.emit(index)

    def highlight(self, current):

        for i, button in enumerate(self.buttons):

            if i == current:

                button.setStyleSheet("""
                QPushButton{
                    background:#4F8CFF;
                    color:white;
                    border:none;
                    border-radius:10px;
                    font-weight:600;
                }
                """)

            else:

                button.setStyleSheet("""
                QPushButton{
                    background:transparent;
                    color:white;
                    border:none;
                    border-radius:10px;
                }

                QPushButton:hover{
                    background:#2A2A2A;
                }
                """)