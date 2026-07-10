from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QScrollArea,
)
from PySide6.QtWidgets import QFileDialog, QLabel
import os
from ui_new.widgets.chat_bubble import ChatBubble
from ui_new.widgets.chat_header import ChatHeader
from services.chat_service import chat_service
from services.conversation_service import conversation_service

class AIConversationWidget(QWidget):

    def __init__(self, mode="chat"):
        super().__init__()

        self.mode = mode

        self.current_ai_bubble = None
        self.stream_buffer = ""
        self.selected_file = None
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # =====================================================
        # Titles
        # =====================================================

        self.titles = {
            "chat": "💬 Athena Chat",
            "math": "🧮 Athena Mathematics",
            "report": "📄 Athena Reports",
            "document": "📚 Athena Documents",
        }

        self.subtitles = {
            "chat": "General AI conversation",
            "math": "Solve equations and mathematical problems",
            "report": "Generate professional reports",
            "document": "Summarize and analyze documents",
        }

        self.placeholders = {
            "chat": "Message Athena...",
            "math": "Enter a mathematical problem...",
            "report": "Generate a report on...",
            "document": "Ask about a document...",
        }

        # =====================================================
        # Header
        # =====================================================

        self.header = ChatHeader(
            title=self.titles.get(
                self.mode,
                "🦉 Athena AI"
            ),
            subtitle=self.subtitles.get(
                self.mode,
                "Your Personal AI Engineer"
            )
        )

        self.layout.addWidget(self.header)

        # =====================================================
        # Chat Area
        # =====================================================

        self.chat_widget = QWidget()

        self.chat_layout = QVBoxLayout(
            self.chat_widget
        )

        self.chat_layout.setSpacing(10)
        self.chat_layout.addStretch()

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(
            self.chat_widget
        )

        self.layout.addWidget(self.scroll)

        # =====================================================
        # Input
        # =====================================================

        input_layout = QHBoxLayout()

        self.input_box = QLineEdit()

        self.input_box.setPlaceholderText(
            self.placeholders.get(
                self.mode,
                "Message Athena..."
            )
        )

        self.attach_btn = QPushButton("📎")

        self.file_label = QLabel("")

        self.file_label.setMinimumWidth(120)

        self.send_btn = QPushButton("Send")

        input_layout.addWidget(self.attach_btn)

        input_layout.addWidget(self.file_label)

        input_layout.addWidget(self.input_box)

        input_layout.addWidget(self.send_btn)

        self.layout.addLayout(
            input_layout
        )

    def reload_messages(self):
        """
    Reload chat bubbles from the active conversation.
    """

    # Remove existing bubbles
        while self.chat_layout.count() > 1:

            item = self.chat_layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()


    # Load current conversation


        conversation = (
            conversation_service.get_active_conversation()
    )


        if conversation is None:
            return


        for message in conversation.messages:

            role = message.get("role", "").lower()

            content = message.get(
            "content",
            ""
        )


            is_user = role == "user"


            self.add_message(
            content,
            is_user
        )


        self.scroll_bottom()

        # =====================================================
        # Signals
        # =====================================================

        self.send_btn.clicked.connect(
            self.send
        )
        self.attach_btn.clicked.connect(
        self.attach_file
)
        self.input_box.returnPressed.connect(
            self.send
        )
        self.load_conversation()

    def load_conversation(self):
        """
    Load the active conversation into the chat UI.
    """

        history = conversation_service.load_history()

        for msg in history:

            role = msg.get("role", "").lower()
            content = msg.get("content", "")

            is_user = role == "user"

            self.add_message(content, is_user)

        self.scroll_bottom()
    # =====================================================
    # Utility
    # =====================================================

    def scroll_bottom(self):

        scrollbar = (
            self.scroll.verticalScrollBar()
        )

        scrollbar.setValue(
            scrollbar.maximum()
        )


    # =====================================================
    # Messages
    # =====================================================

    def add_message(
        self,
        text,
        is_user
    ):

        bubble = ChatBubble(
            text,
            is_user
        )

        self.chat_layout.insertWidget(
            self.chat_layout.count() - 1,
            bubble
        )

        self.scroll_bottom()

        return bubble
    def attach_file(self):

        file_path, _ = QFileDialog.getOpenFileName(
        self,
        "Select File",
        "",
        "Supported Files (*.txt *.docx *.pdf *.py *.png *.jpg);;All Files (*)"
    )

        if file_path:

            self.selected_file = file_path

            self.file_label.setText(
            os.path.basename(file_path)
        )

    # =====================================================
    # Send
    # =====================================================

    def send(self):

        message = self.input_box.text().strip()

        if not message:
            return

        self.add_message(
        message,
        True
    )

    # Save the selected file BEFORE clearing anything
        selected_file = self.selected_file

        self.input_box.clear()

        self.stream_buffer = ""

        self.current_ai_bubble = self.add_message(
        "Athena is thinking...",
        False
    )

        chat_service.stream_message(
            message=message,
        file_path=selected_file,
        chunk_callback=self.on_chunk,
        finished_callback=self.on_finished,
        error_callback=self.on_error,
        started_callback=self.on_started,
    )

    # Reset file selection AFTER sending
        self.selected_file = None
        self.file_label.setText("")

    # =====================================================
    # Streaming Callbacks
    # =====================================================

    def on_started(self):

        if self.current_ai_bubble:

            self.current_ai_bubble.set_text(
                "Athena is thinking..."
            )


    def on_chunk(self, chunk):
        self.stream_buffer += chunk


        if self.current_ai_bubble:

            self.current_ai_bubble.set_text(
                self.stream_buffer
            )


        self.scroll_bottom()


    def on_finished(self, response):

        self.stream_buffer = response


        if self.current_ai_bubble:

            self.current_ai_bubble.set_text(
                response
            )


        self.scroll_bottom()


    def on_error(self, error):

        if self.current_ai_bubble:

            self.current_ai_bubble.set_text(
                f"⚠️ {error}"
            )


        self.scroll_bottom()