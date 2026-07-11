from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QScrollArea,
    QFileDialog,
    QLabel,
)

from PySide6.QtCore import Signal

import os

from ui_new.widgets.chat_bubble import ChatBubble
from ui_new.widgets.chat_header import ChatHeader
from ui_new.widgets.attachment_preview import AttachmentPreview

from services.chat_service import chat_service
from services.conversation_service import conversation_service


class AIConversationWidget(QWidget):

    conversation_updated = Signal()

    def __init__(self, mode="chat"):
        super().__init__()

        self.mode = mode

        self.current_ai_bubble = None
        self.stream_buffer = ""

        self.selected_file = None
        self.preview_widget: AttachmentPreview | None = None

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
                "🦉 Athena AI",
            ),
            subtitle=self.subtitles.get(
                self.mode,
                "Your Personal AI Engineer",
            ),
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
        # Attachment Preview
        # =====================================================

        self.preview_container = QVBoxLayout()
        self.layout.addLayout(
            self.preview_container
        )

        # =====================================================
        # Input Area
        # =====================================================

        input_layout = QHBoxLayout()

        self.attach_btn = QPushButton("📎")

        self.file_label = QLabel("")

        self.file_label.setMinimumWidth(150)

        self.file_label.setStyleSheet(
            """
            color:#888;
            font-size:11px;
            """
        )

        self.input_box = QLineEdit()

        self.input_box.setPlaceholderText(
            self.placeholders.get(
                self.mode,
                "Message Athena...",
            )
        )

        self.send_btn = QPushButton("Send")

        input_layout.addWidget(
            self.attach_btn
        )

        input_layout.addWidget(
            self.file_label
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

        self.attach_btn.clicked.connect(
            self.attach_file
        )

        self.input_box.returnPressed.connect(
            self.send
        )

        # =====================================================
        # Initial Conversation
        # =====================================================

        self.load_conversation()

        # =====================================================
    # Reload Messages
    # =====================================================

    def reload_messages(self):
        """
        Reload all messages from the active conversation.
        """

        # Remove every bubble except the stretch
        while self.chat_layout.count() > 1:

            item = self.chat_layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

        conversation = (
            conversation_service.get_active_conversation()
        )

        if conversation is None:
            return

        for message in conversation.messages:

            role = message.get(
                "role",
                ""
            ).lower()

            content = message.get(
                "content",
                ""
            )

            self.add_message(
                content,
                role == "user"
            )

        self.scroll_bottom()

    # =====================================================
    # Load Conversation
    # =====================================================

    def load_conversation(self):
        """
        Load the currently active conversation.
        """

        history = (
            conversation_service.load_history()
        )

        for message in history:

            role = message.get(
                "role",
                ""
            ).lower()

            content = message.get(
                "content",
                ""
            )

            self.add_message(
                content,
                role == "user"
            )

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
    # Message Bubble
    # =====================================================

    def add_message(
        self,
        text: str,
        is_user: bool,
    ):

        bubble = ChatBubble(
            text=text,
            is_user=is_user,
        )

        self.chat_layout.insertWidget(
            self.chat_layout.count() - 1,
            bubble,
        )

        bubble.show()

        self.scroll_bottom()

        return bubble
    
        # =====================================================
    # Attach File
    # =====================================================

    def attach_file(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",
            (
                "Supported Files "
                "(*.txt *.docx *.pdf "
                "*.py *.cpp *.c *.h *.hpp "
                "*.java *.js *.ts *.cs *.go *.rs "
                "*.php *.html *.css *.json *.xml "
                "*.yaml *.yml *.toml "
                "*.png *.jpg *.jpeg *.bmp);;"
                "All Files (*)"
            ),
        )

        if not file_path:
            return

        self.selected_file = file_path

        self.file_label.setText(
            os.path.basename(file_path)
        )

        # Remove previous preview

        if self.preview_widget:

            self.preview_container.removeWidget(
                self.preview_widget
            )

            self.preview_widget.deleteLater()

            self.preview_widget = None

        # Create new preview

        self.preview_widget = AttachmentPreview(
            file_path
        )

        self.preview_widget.removed.connect(
            self.remove_attachment
        )

        self.preview_container.addWidget(
            self.preview_widget
        )

        self.input_box.setFocus()

    # =====================================================
    # Remove Attachment
    # =====================================================

    def remove_attachment(self):

        self.selected_file = None

        self.file_label.setText("")

        if self.preview_widget:

            self.preview_container.removeWidget(
                self.preview_widget
            )

            self.preview_widget.deleteLater()

            self.preview_widget = None

        self.input_box.setFocus()

    # =====================================================
    # Send Message
    # =====================================================

    def send(self):

        message = self.input_box.text().strip()

        if not message:
            return

        # User bubble

        self.add_message(
            message,
            True,
        )

        # Preserve attachment

        selected_file = self.selected_file

        # Reset input

        self.input_box.clear()

        self.stream_buffer = ""

        # Prevent duplicate sends

        self.send_btn.setEnabled(False)

        self.attach_btn.setEnabled(False)

        # Placeholder bubble

        self.current_ai_bubble = self.add_message(
            "Athena is thinking...",
            False,
        )

        # Stream response

        chat_service.stream_message(
            message=message,
            file_path=selected_file,
            chunk_callback=self.on_chunk,
            finished_callback=self.on_finished,
            error_callback=self.on_error,
            started_callback=self.on_started,
        )

        # Clear attachment UI

        self.remove_attachment()

        # =====================================================
    # Streaming Callbacks
    # =====================================================

    def on_started(self):
        """
        Called when the worker starts generating.
        """

        if self.current_ai_bubble:

            self.current_ai_bubble.set_text(
                "Athena is thinking..."
            )

        self.scroll_bottom()

    def on_chunk(self, chunk: str):
        """
        Called whenever a new streamed chunk arrives.
        """

        self.stream_buffer += chunk

        if self.current_ai_bubble:

            self.current_ai_bubble.set_text(
                self.stream_buffer
            )

        self.scroll_bottom()

    def on_finished(self, response: str):
        """
        Called after streaming completes.
        """

        self.stream_buffer = response

        if self.current_ai_bubble:

            self.current_ai_bubble.set_text(
                response
            )

        # Re-enable controls

        self.send_btn.setEnabled(True)
        self.attach_btn.setEnabled(True)

        self.input_box.setFocus()

        self.scroll_bottom()

        self.conversation_updated.emit()

    def on_error(self, error: str):
        """
        Called when generation fails.
        """

        if self.current_ai_bubble:

            self.current_ai_bubble.set_text(
                f"⚠️ {error}"
            )

        # Re-enable controls

        self.send_btn.setEnabled(True)
        self.attach_btn.setEnabled(True)

        self.input_box.setFocus()

        self.scroll_bottom()