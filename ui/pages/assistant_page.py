from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt


class AssistantPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        label = QLabel("Assistant Module")
        label.setAlignment(Qt.AlignCenter)

        label.setStyleSheet("""
            font-size:30px;
            font-weight:bold;
        """)

        layout.addWidget(label)

        self.setLayout(layout)  