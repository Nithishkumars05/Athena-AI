from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, Signal


class FeatureCard(QFrame):

    clicked = Signal(str)

    def __init__(self, icon, title, description, page_key, parent=None):
        super().__init__(parent)

        self.page_key = page_key

        self.setCursor(Qt.PointingHandCursor)

        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
            }

            QFrame:hover {
                border: 1px solid #2563EB;
                background-color: #F9FAFB;
            }
        """)

        layout = QVBoxLayout()

        self.icon_label = QLabel(icon)
        self.icon_label.setStyleSheet("font-size:24px;")

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-size:18px; font-weight:bold;")

        self.desc_label = QLabel(description)
        self.desc_label.setStyleSheet("font-size:13px; color:#6B7280;")

        layout.addWidget(self.icon_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.desc_label)

        self.setLayout(layout)
        self.setFixedSize(250, 120)

    def mousePressEvent(self, event):
        self.clicked.emit(self.page_key)