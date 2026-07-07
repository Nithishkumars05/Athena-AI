from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QScrollArea,
    QLabel
)
from ui_new.widgets.chat_bubble import ChatBubble
from services.chat_service import chat_service
from ui_new.widgets.chat_header import ChatHeader

class ChatPage(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.header = ChatHeader()
        self.layout.addWidget(self.header)
        # =========================
        # Chat display area
        # =========================
        self.chat_area_widget = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_area_widget)
        self.chat_layout.addStretch()

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.chat_area_widget)

        self.layout.addWidget(self.scroll)

        # =========================
        # Input area
        # =========================
        input_row = QHBoxLayout()

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Message Athena AI...")

        self.send_btn = QPushButton("Send")

        input_row.addWidget(self.input_box)
        input_row.addWidget(self.send_btn)

        self.layout.addLayout(input_row)

        # =========================
        # Signals
        # =========================
        self.send_btn.clicked.connect(self.send)
        self.input_box.returnPressed.connect(self.send)

    # =========================
    # Message rendering
    # =========================
    def add_message(self, text, is_user=True):

        bubble = ChatBubble(text, is_user)

        self.chat_layout.insertWidget(
            self.chat_layout.count() - 1,
            bubble
    )

        self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().maximum()
    )

    # =========================
    # Async send flow
    # =========================
    def send(self):
        message = self.input_box.text().strip()
        if not message:
            return

        # show user message
        self.add_message(message, True)
        self.input_box.clear()

        # show temporary thinking message
        thinking_label = QLabel("Athena is thinking...")
        thinking_label.setStyleSheet("""
            background-color: #444;
            color: white;
            padding: 10px;
            border-radius: 10px;
            margin: 5px;
        """)

        self.chat_layout.insertWidget(
            self.chat_layout.count() - 1,
            thinking_label
        )

        # callbacks
        def on_response(response):
            thinking_label.setText(response)

        def on_error(error):
            thinking_label.setText(f"Error: {error}")

        # async call via service layer
        chat_service.send_message(message, on_response, on_error)