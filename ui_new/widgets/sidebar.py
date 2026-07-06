from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel


class Sidebar(QWidget):

    page_changed = Signal(int)

    def __init__(self):
        super().__init__()

        self.setFixedWidth(220)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(10)

        # -------------------------
        # Logo
        # -------------------------
        title = QLabel("🦉 ATHENA AI")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Engineering Assistant")
        subtitle.setObjectName("Subtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(25)

        # -------------------------
        # Navigation Buttons
        # -------------------------
        self.buttons = []

        pages = [
            "🏠 Home",
            "💬 AI Chat",
            "🧮 Mathematics",
            "📄 Reports",
            "📚 Documents",
            "📁 Projects",
            "⚙ Settings"
        ]

        for index, page in enumerate(pages):

            button = QPushButton(page)
            button.setFixedHeight(42)

            button.clicked.connect(
                lambda checked=False, i=index: self.change_page(i)
            )

            layout.addWidget(button)

            self.buttons.append(button)

        layout.addStretch()

    def change_page(self, index):
        self.page_changed.emit(index)