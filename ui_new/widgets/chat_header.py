from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QFrame
)
from PySide6.QtCore import Qt


class ChatHeader(QFrame):

    def __init__(self):
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

        # Left side
        left = QVBoxLayout()

        title = QLabel("🦉 Athena AI")
        title.setObjectName("title")

        subtitle = QLabel("Your Personal AI Engineer")
        subtitle.setObjectName("subtitle")

        left.addWidget(title)
        left.addWidget(subtitle)

        # Right side
        status = QLabel("● Online")
        status.setObjectName("status")
        status.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout.addLayout(left)
        layout.addStretch()
        layout.addWidget(status)