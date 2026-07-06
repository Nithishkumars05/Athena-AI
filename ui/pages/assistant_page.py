from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QTextBrowser, QHBoxLayout
)
from PySide6.QtCore import Qt

from agents.chat_agent import chat


class AssistantPage(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        # Chat display (better than QTextEdit)
        self.chat_area = QTextBrowser()
        self.chat_area.setStyleSheet("""
            font-size:14px;
            padding:10px;
            background:#F9FAFB;
        """)

        # Input row
        input_row = QHBoxLayout()

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Ask Athena something...")

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.handle_send)

        input_row.addWidget(self.input_box)
        input_row.addWidget(self.send_button)

        self.layout.addWidget(self.chat_area)
        self.layout.addLayout(input_row)

        self.setLayout(self.layout)

        # Welcome message
        self.add_message("Athena", "Hello! How can I help you today?")

    def add_message(self, sender, message):

        if sender == "You":
            formatted = f"""
            <div style='text-align:right; margin:10px;'>
                <span style='background:#2563EB; color:white; padding:8px 12px; border-radius:10px; display:inline-block;'>
                    {message}
                </span>
            </div>
            """
        else:
            formatted = f"""
            <div style='text-align:left; margin:10px;'>
                <span style='background:#E5E7EB; color:black; padding:8px 12px; border-radius:10px; display:inline-block;'>
                    {message}
                </span>
            </div>
            """

        self.chat_area.append(formatted)

    def handle_send(self):

        user_text = self.input_box.text().strip()

        if not user_text:
            return

        self.add_message("You", user_text)

        try:
            response = chat("User", user_text)
        except Exception as e:
            response = f"Error: {str(e)}"

        self.add_message("Athena", response)

        self.input_box.clear()