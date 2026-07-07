from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QFrame
)
from PySide6.QtCore import Qt


class ChatBubble(QWidget):

    def __init__(self, text: str, is_user: bool):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        bubble = QFrame()
        bubble_layout = QHBoxLayout(bubble)

        label = QLabel(text)
        label.setWordWrap(True)

        bubble_layout.addWidget(label)

        bubble.setMaximumWidth(600)

        if is_user:
            bubble.setStyleSheet("""
                QFrame{
                    background:#2B6FFF;
                    border-radius:15px;
                    padding:10px;
                }
                QLabel{
                    color:white;
                    font-size:14px;
                }
            """)
            layout.addStretch()
            layout.addWidget(bubble)

        else:
            bubble.setStyleSheet("""
                QFrame{
                    background:#353535;
                    border-radius:15px;
                    padding:10px;
                }
                QLabel{
                    color:white;
                    font-size:14px;
                }
            """)
            layout.addWidget(bubble)
            layout.addStretch()