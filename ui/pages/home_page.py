from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt


class HomePage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        greeting = QLabel("Good Afternoon!")
        greeting.setAlignment(Qt.AlignCenter)

        title = QLabel("Welcome to Athena AI")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel(
            "Your Intelligent Engineering Workspace"
        )
        subtitle.setAlignment(Qt.AlignCenter)

        greeting.setStyleSheet(
            "font-size:20px; color:#6B7280;"
        )

        title.setStyleSheet(
            "font-size:36px; font-weight:bold;"
        )

        subtitle.setStyleSheet(
            "font-size:18px; color:#6B7280;"
        )

        layout.addStretch()
        layout.addWidget(greeting)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()

        self.setLayout(layout)