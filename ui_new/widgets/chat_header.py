from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QFrame
)
from PySide6.QtCore import Qt


class ChatHeader(QFrame):

    def __init__(
        self,
        title="🦉 Athena AI",
        subtitle="Your Personal AI Engineer"
    ):
        super().__init__()

        self.setFixedHeight(80)

        self.setStyleSheet("""
            QFrame{
                background-color:#202123;
                border-bottom:1px solid #3a3a3a;
            }

            QLabel#title{
                color:white;
                font-size:18px;
                font-weight:bold;
            }

            QLabel#subtitle{
                color:#A0A0A0;
                font-size:12px;
            }

            QLabel#status{
                color:#42d66b;
                font-size:13px;
                font-weight:bold;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)

        # ==========================
        # Left
        # ==========================

        left = QVBoxLayout()

        self.title = QLabel(title)
        self.title.setObjectName("title")

        self.subtitle = QLabel(subtitle)
        self.subtitle.setObjectName("subtitle")

        left.addWidget(self.title)
        left.addWidget(self.subtitle)

        # ==========================
        # Right
        # ==========================

        self.status = QLabel("● Online")
        self.status.setObjectName("status")
        self.status.setAlignment(
            Qt.AlignRight | Qt.AlignVCenter
        )

        layout.addLayout(left)
        layout.addStretch()
        layout.addWidget(self.status)

    # =====================================
    # Public API
    # =====================================

    def set_title(self, text: str):
        self.title.setText(text)

    def set_subtitle(self, text: str):
        self.subtitle.setText(text)

    def set_status(self, text: str):
        self.status.setText(text)