from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QTextBrowser,
    QHBoxLayout,
    QVBoxLayout,
    QFrame
)
from PySide6.QtCore import Qt
from datetime import datetime


class ChatBubble(QWidget):

    def __init__(self, text: str, is_user: bool):
        super().__init__()

        self.is_user = is_user

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(15, 5, 15, 5)

        self.bubble = QFrame()
        self.bubble.setMaximumWidth(700)

        bubble_layout = QVBoxLayout(self.bubble)
        bubble_layout.setContentsMargins(15, 10, 15, 10)

        # Sender
        self.sender = QLabel(
            "You" if is_user else "🦉 Athena"
        )
        self.sender.setStyleSheet("""
            color:#AAAAAA;
            font-size:11px;
            font-weight:bold;
        """)

        # Message
        if is_user:

            self.label = QLabel(text)

            self.label.setWordWrap(True)

            self.label.setTextInteractionFlags(
        Qt.TextSelectableByMouse
    )

        else:

            self.label = QTextBrowser()

            self.label.setOpenExternalLinks(True)

            self.label.setFrameShape(
        QFrame.NoFrame
    )

            self.label.setReadOnly(True)

            self.label.setHorizontalScrollBarPolicy(
        Qt.ScrollBarAlwaysOff
    )

            self.label.setVerticalScrollBarPolicy(
        Qt.ScrollBarAlwaysOff
    )

            self.label.setStyleSheet("""
        QTextBrowser{
            background:transparent;
            color:white;
            border:none;
            font-size:14px;
        }
    """)

            self.label.setMarkdown(text)

        # Time
        self.time = QLabel(
            datetime.now().strftime("%H:%M")
        )
        self.time.setAlignment(Qt.AlignRight)
        self.time.setStyleSheet("""
            color:#888888;
            font-size:10px;
        """)

        bubble_layout.addWidget(self.sender)
        bubble_layout.addWidget(self.label)
        bubble_layout.addWidget(self.time)

        if is_user:

            self.bubble.setStyleSheet("""
                QFrame{
                    background:#2B6FFF;
                    border-radius:18px;
                }

                QLabel{
                    color:white;
                    font-size:14px;
                }
            """)

            main_layout.addStretch()
            main_layout.addWidget(self.bubble)

        else:

            self.bubble.setStyleSheet("""
                QFrame{
                    background:#303030;
                    border-radius:18px;
                }

                QLabel{
                    color:white;
                    font-size:14px;
                }
            """)

            main_layout.addWidget(self.bubble)
            main_layout.addStretch()

    def set_text(self, text: str):

        if self.is_user:

            self.label.setText(text)
            self.label.adjustSize()

        else:

            self.label.setMarkdown(text)
            self.label.document().adjustSize()

        self.bubble.adjustSize()
        self.adjustSize()
        self.updateGeometry()

        if self.parentWidget():
            self.parentWidget().adjustSize()