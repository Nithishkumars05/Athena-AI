from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QScrollArea,
)

from ui_new.widgets.chat_bubble import ChatBubble
from ui_new.widgets.chat_header import ChatHeader
from services.chat_service import chat_service


class AIConversationWidget(QWidget):

    def __init__(self, mode="chat"):
        super().__init__()

        self.mode = mode

        self.current_ai_bubble = None
        self.stream_buffer = ""

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

        self.send_btn = QPushButton(
            "Send"
        )

        input_layout.addWidget(
            self.input_box
        )

        input_layout.addWidget(
            self.send_btn
        )

        self.layout.addLayout(
            input_layout
        )

        # =====================================================
        # Signals
        # =====================================================

        self.send_btn.clicked.connect(
            self.send
        )

        self.input_box.returnPressed.connect(
            self.send
        )


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


    # =====================================================
    # Send
    # =====================================================

    def send(self):

        message = (
            self.input_box.text()
            .strip()
        )

        if not message:
            return


        self.add_message(
            message,
            True
        )

        self.input_box.clear()


        self.stream_buffer = ""


        self.current_ai_bubble = self.add_message(
            "Athena is thinking...",
            False
        )


        chat_service.stream_message(
            message=message,
            chunk_callback=self.on_chunk,
            finished_callback=self.on_finished,
            error_callback=self.on_error,
            started_callback=self.on_started,
        )


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