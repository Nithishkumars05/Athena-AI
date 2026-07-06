from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGridLayout
from PySide6.QtCore import Qt, Signal

from ui.widgets.feature_card import FeatureCard


class HomePage(QWidget):

    navigate = Signal(str)

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        title = QLabel("Good Afternoon, Nithish")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:22px; font-weight:bold;")

        subtitle = QLabel("Welcome to Athena AI - Your Engineering Workspace")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size:14px; color:#6B7280;")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        grid = QGridLayout()

        cards = [
            FeatureCard("💬", "Assistant", "Talk with Athena", "assistant"),
            FeatureCard("🧮", "Mathematics", "Solve equations instantly", "math"),
            FeatureCard("📄", "Reports", "Generate professional reports", "report"),
            FeatureCard("📚", "Documents", "Summarize PDFs & files", "documents"),
        ]

        positions = [(0,0), (0,1), (1,0), (1,1)]

        for card, pos in zip(cards, positions):
            card.clicked.connect(self.navigate.emit)
            grid.addWidget(card, pos[0], pos[1])

        main_layout.addLayout(grid)

        footer = QLabel("Athena AI v5.0 • Offline Ready")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color:#9CA3AF; font-size:12px;")

        main_layout.addWidget(footer)

        self.setLayout(main_layout)