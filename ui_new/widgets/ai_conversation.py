from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QPushButton,
    QScrollArea,
    QFileDialog,
    QLabel,
    QFrame,
)

from PySide6.QtCore import Qt, Signal, QEvent
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
        self.preview_widget = None

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # ==========================================
        # Titles
        # ==========================================

        self.titles = {
            "chat": "💬 Athena Chat",
            "math": "🧮 Athena Mathematics",
            "report": "📄 Athena Reports",
            "document": "📚 Athena Documents",
        }

        self.subtitles = {
            "chat": "General AI conversation",
            "math": "Solve equations",
            "report": "Generate reports",
            "document": "Analyze documents",
        }

        self.placeholders = {
            "chat": "Message Athena...",
            "math": "Solve...",
            "report": "Generate report...",
            "document": "Ask about your document...",
        }

        # ==========================================
        # Header
        # ==========================================

        self.header = ChatHeader(
            title=self.titles.get(
                self.mode,
                "Athena AI"
            ),
            subtitle=self.subtitles.get(
                self.mode,
                ""
            ),
        )

        self.layout.addWidget(self.header)

        # ==========================================
        # Chat Area
        # ==========================================

        self.chat_widget = QWidget()

        self.chat_layout = QVBoxLayout(
            self.chat_widget
        )

        self.chat_layout.setSpacing(12)
        self.chat_layout.setContentsMargins(
            15,
            15,
            15,
            15
        )

        self.chat_layout.addStretch()

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(True)

        self.scroll.setWidget(
            self.chat_widget
        )

        self.scroll.setFrameShape(
            QFrame.NoFrame
        )

        self.layout.addWidget(
            self.scroll,
            1
        )

        # ==========================================
        # Bottom Composer
        # ==========================================

        self.bottom_panel = QFrame()

        self.bottom_panel.setStyleSheet("""
        QFrame{
            background:#17181E;
            border-top:1px solid #303030;
        }
        """)

        self.bottom_layout = QVBoxLayout(
            self.bottom_panel
        )

        self.bottom_layout.setContentsMargins(
            10,
            10,
            10,
            10
        )

        self.bottom_layout.setSpacing(8)

        # ==========================================
        # Attachment Preview
        # ==========================================

        self.preview_container = QVBoxLayout()

        self.bottom_layout.addLayout(
            self.preview_container
        )

        # ==========================================
        # Input Row
        # ==========================================

        input_layout = QHBoxLayout()

        self.attach_btn = QPushButton("📎")

        self.input_box = QTextEdit()

        self.input_box.setPlaceholderText(
            self.placeholders.get(
                self.mode,
                "Message Athena..."
            )
        )

        self.input_box.installEventFilter(self)
        self.input_box.textChanged.connect(
            self.resize_input_box
)

        self.input_box.setMinimumHeight(45)
        self.input_box.setMaximumHeight(120)

        self.input_box.setStyleSheet("""
        QTextEdit{
            border-radius:12px;
            padding:8px;
            font-size:14px;
        }
        """)

        self.send_btn = QPushButton("Send")

        self.file_label = QLabel()

        input_layout.addWidget(
            self.attach_btn
        )

        input_layout.addWidget(
            self.file_label
        )

        input_layout.addWidget(
            self.input_box,
            1
        )

        input_layout.addWidget(
            self.send_btn
        )

        self.bottom_layout.addLayout(
            input_layout
        )

        self.layout.addWidget(
            self.bottom_panel
        )

        # ==========================================
        # Signals
        # ==========================================

        self.send_btn.clicked.connect(
            self.send
        )

        self.attach_btn.clicked.connect(
            self.attach_file
        )

        self.load_conversation()

        # =====================================================
    # Conversation Loading
    # =====================================================

    def reload_messages(self):

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


    def load_conversation(self):

        history = (
            conversation_service.load_history()
        )

        for msg in history:

            role = msg.get(
                "role",
                ""
            ).lower()

            content = msg.get(
                "content",
                ""
            )

            self.add_message(
                content,
                role == "user"
            )

        self.scroll_bottom()


    # =====================================================
    # Utilities
    # =====================================================

    def scroll_bottom(self):

        scrollbar = self.scroll.verticalScrollBar()

        scrollbar.setValue(
            scrollbar.maximum()
        )


    # =====================================================
    # Chat Messages
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
    # Attachment
    # =====================================================

    def attach_file(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",
            "Supported Files (*.txt *.docx *.pdf *.py *.png *.jpg *.jpeg *.bmp);;All Files (*)"
        )

        if not file_path:
            return

        self.selected_file = file_path

        self.file_label.setText(
            os.path.basename(file_path)
        )

        if self.preview_widget:

            self.preview_container.removeWidget(
                self.preview_widget
            )

            self.preview_widget.deleteLater()

        self.preview_widget = AttachmentPreview(
            file_path
        )

        self.preview_widget.removed.connect(
            self.remove_attachment
        )

        self.preview_container.addWidget(
            self.preview_widget
        )


    def remove_attachment(self):

        self.selected_file = None

        self.file_label.clear()

        if self.preview_widget:

            self.preview_container.removeWidget(
                self.preview_widget
            )

            self.preview_widget.deleteLater()

            self.preview_widget = None

        # =====================================================
    # Send Message
    # =====================================================

    def send(self):

        message = self.input_box.toPlainText().strip()

        if not message:
            return

        self.add_message(
            message,
            True
        )

        selected_file = self.selected_file

        self.input_box.clear()

        self.input_box.setFixedHeight(45)

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

        self.remove_attachment()


    # =====================================================
    # Input Box Auto Resize
    # =====================================================

    def resize_input_box(self):

        document = self.input_box.document()

        height = int(document.size().height()) + 12

        height = max(45, min(height, 120))

        self.input_box.setFixedHeight(height)


        # =====================================================
    # Enter = Send
    # Shift+Enter = New Line
    # =====================================================

    def eventFilter(self, obj, event):

        if obj == self.input_box:

            if event.type() == QEvent.KeyPress:

                if event.key() in (
                    Qt.Key_Return,
                    Qt.Key_Enter
                ):

                    if event.modifiers() == Qt.ShiftModifier:

                        return False

                    self.send()

                    return True

        return super().eventFilter(obj, event)
    
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

        self.conversation_updated.emit()


    def on_error(self, error):

        if self.current_ai_bubble:
            self.current_ai_bubble.set_text(
                f"⚠️ {error}"
            )

        self.scroll_bottom()