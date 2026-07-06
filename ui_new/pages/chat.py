from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QScrollArea,
    QLabel
)

from services.chat_service import send_message


class ChatPage(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

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
    # Message UI
    # =========================
    def add_message(self, text, is_user=True):

        label = QLabel(text)
        label.setWordWrap(True)

        if is_user:
            label.setStyleSheet("""
                background-color: #2b6fff;
                color: white;
                padding: 10px;
                border-radius: 10px;
                margin: 5px;
            """)
        else:
            label.setStyleSheet("""
                background-color: #2e2e2e;
                color: white;
                padding: 10px;
                border-radius: 10px;
                margin: 5px;
            """)

        # insert above stretch
        self.chat_layout.insertWidget(
            self.chat_layout.count() - 1,
            label
        )

        # auto scroll to bottom
        self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().maximum()
        )

    # =========================
    # Send message flow
    # =========================
    def send(self):
        message = self.input_box.text().strip()
        if not message:
            return

        # show user message
        self.add_message(message, True)
        self.input_box.clear()

        # get response from service layer
        response = send_message(message)

        # show AI response
        self.add_message(response, False)