from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QScrollArea
)
from PySide6.QtCore import Qt

from ui_new.widgets.chat_bubble import ChatBubble
from ui_new.widgets.chat_header import ChatHeader
from services.chat_service import chat_service


class ChatPage(QWidget):

    def __init__(self):
        super().__init__()

        self.current_ai_bubble = None

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # =========================
        # Header
        # =========================
        self.header = ChatHeader()
        self.layout.addWidget(self.header)

        # =========================
        # Chat Area
        # =========================
        self.chat_widget = QWidget()

        self.chat_layout = QVBoxLayout(self.chat_widget)
        self.chat_layout.setSpacing(10)
        self.chat_layout.addStretch()

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.chat_widget)

        self.layout.addWidget(self.scroll)

        # =========================
        # Input Area
        # =========================
        input_layout = QHBoxLayout()

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Message Athena AI...")

        self.send_btn = QPushButton("Send")

        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.send_btn)

        self.layout.addLayout(input_layout)

        # =========================
        # Signals
        # =========================
        self.send_btn.clicked.connect(self.send)
        self.input_box.returnPressed.connect(self.send)

    # ======================================================
    # Utility
    # ======================================================

    def scroll_bottom(self):
        self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().maximum()
        )

    # ======================================================
    # Add Message
    # ======================================================

    def add_message(self, text, is_user):

        bubble = ChatBubble(text, is_user)

        self.chat_layout.insertWidget(
            self.chat_layout.count() - 1,
            bubble
        )

        self.scroll_bottom()

        return bubble

    # ======================================================
    # Send Message
    # ======================================================

    def send(self):

        message = self.input_box.text().strip()

        if not message:
            return

        # User bubble
        self.add_message(message, True)

        self.input_box.clear()

        # Athena placeholder
        self.current_ai_bubble = self.add_message(
            "Athena is thinking...",
            False
        )

        chat_service.send_message(
            message,
            self.on_response,
            self.on_error
        )

    # ======================================================
    # Callbacks
    # ======================================================

    def on_response(self, response):

        if self.current_ai_bubble:
            self.current_ai_bubble.set_text(response)

        self.scroll_bottom()

    def on_error(self, error):

        if self.current_ai_bubble:
            self.current_ai_bubble.set_text(
                f"⚠️ {error}"
            )

        self.scroll_bottom()