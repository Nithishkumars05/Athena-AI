from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QScrollArea,
    QFileDialog,
    QLabel,
    QFrame,
)

from PySide6.QtCore import (
    Signal,
    Qt,
    QTimer,
    QSize
)

from PySide6.QtGui import QIcon

import os


from ui_new.widgets.chat_bubble import ChatBubble
from ui_new.widgets.chat_header import ChatHeader
from ui_new.widgets.attachment_preview import AttachmentPreview
from ui_new.widgets.message_input import MessageInput


from services.chat_service import chat_service
from services.conversation_service import conversation_service



class AIConversationWidget(QWidget):


    conversation_updated = Signal()



    def __init__(
        self,
        mode="chat"
    ):

        super().__init__()


        self.mode = mode


        self.current_ai_bubble = None

        self.stream_buffer = ""

        self.selected_file = None

        self.preview_widget = None



        # ==============================
        # Main Layout
        # ==============================


        self.layout = QVBoxLayout(
            self
        )


        self.layout.setContentsMargins(
            0,
            0,
            0,
            0
        )


        self.layout.setSpacing(
            0
        )



        # ==============================
        # Header
        # ==============================


        self.header = ChatHeader(

            title="💬 Athena Chat",

            subtitle="General AI conversation"

        )


        self.layout.addWidget(
            self.header
        )



        # ==============================
        # Chat Area
        # ==============================


        self.chat_widget = QWidget()


        self.chat_layout = QVBoxLayout(
            self.chat_widget
        )


        self.chat_layout.setContentsMargins(
            15,
            15,
            15,
            15
        )


        self.chat_layout.setSpacing(
            12
        )


        self.chat_layout.addStretch()



        self.scroll = QScrollArea()


        self.scroll.setWidgetResizable(
            True
        )


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

            # ==============================
        # Composer Area
        # ==============================


        self.bottom_panel = QFrame()


        self.bottom_layout = QVBoxLayout(
            self.bottom_panel
        )


        self.bottom_layout.setContentsMargins(
            10,
            10,
            10,
            10
        )


        # ------------------------------
        # Attachment Preview
        # ------------------------------

        self.preview_container = QVBoxLayout()


        self.bottom_layout.addLayout(
            self.preview_container
        )



        # ------------------------------
        # Composer
        # ------------------------------


        self.composer = QFrame()


        composer_layout = QHBoxLayout(
            self.composer
        )


        composer_layout.setContentsMargins(
            10,
            8,
            10,
            8
        )


        composer_layout.setSpacing(
            8
        )



        # Attachment button

        self.attach_btn = QPushButton()


        self.attach_btn.setIcon(
            QIcon(
                "assets/icons/attach.svg"
            )
        )


        self.attach_btn.setIconSize(
            QSize(20,20)
        )


        self.attach_btn.setFixedSize(
            36,
            36
        )



        # Message input

        self.input_box = MessageInput()


        self.input_box.setPlaceholderText(
            "Message Athena..."
        )


        self.input_box.sendRequested.connect(
            self.send
        )



        # Send button


        self.send_btn = QPushButton()


        self.send_btn.setIcon(
            QIcon(
                "assets/icons/send.svg"
            )
        )


        self.send_btn.setIconSize(
            QSize(20,20)
        )


        self.send_btn.setFixedSize(
            38,
            38
        )



        self.file_label = QLabel()



        composer_layout.addWidget(
            self.attach_btn
        )


        composer_layout.addWidget(
            self.file_label
        )


        composer_layout.addWidget(
            self.input_box,
            1
        )


        composer_layout.addWidget(
            self.send_btn
        )



        self.bottom_layout.addWidget(
            self.composer
        )


        self.layout.addWidget(
            self.bottom_panel
        )



        # ==============================
        # Signals
        # ==============================


        self.send_btn.clicked.connect(
            self.send
        )


        self.attach_btn.clicked.connect(
            self.attach_file
        )



        # Load active conversation

        self.load_conversation()



        QTimer.singleShot(
            0,
            self.input_box.setFocus
        )



    # ==================================================
    # Conversation Loading
    # ==================================================


    def load_conversation(self):


        self.reload_messages()



    def reload_messages(self):


        conversation = (
            conversation_service
            .get_active_conversation()
        )


        if not conversation:

            return



        self.clear_messages()



        for message in conversation.messages:


            role = message.get(
                "role",
                ""
            ).lower()


            content = message.get(
                "content",
                ""
            )


            if not content:

                continue



            self.add_message(

                content,

                role == "user"

            )



        self.scroll_bottom()



    # ==================================================
    # Clear Chat
    # ==================================================


    def clear_messages(self):


        while self.chat_layout.count() > 1:


            item = (
                self.chat_layout
                .takeAt(0)
            )


            widget = item.widget()


            if widget:


                widget.deleteLater()



    # ==================================================
    # Add Message
    # ==================================================


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



    # ==================================================
    # Scroll
    # ==================================================


    def scroll_bottom(self):


        scrollbar = (
            self.scroll
            .verticalScrollBar()
        )


        scrollbar.setValue(

            scrollbar.maximum()

        )
    # ==================================================
# Attachment Handling
# ==================================================


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

            os.path.basename(
                file_path
            )

        )




    def remove_attachment(self):


        self.selected_file = None


        self.file_label.clear()



# ==================================================
# Send Message
# ==================================================


    def send(self):


        message = (
            self.input_box
            .toPlainText()
            .strip()
        )


        if not message:

            return



        # Display user message

        self.add_message(

            message,

            True

        )



        # Save user message

        conversation_service.save_user_message(

            "",

            message

        )



        selected_file = self.selected_file



        self.input_box.clear()



        self.stream_buffer = ""



        # Temporary AI bubble

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



# ==================================================
# Streaming
# ==================================================


    def on_started(self):


        if self.current_ai_bubble:


            self.current_ai_bubble.set_text(

                "Athena is thinking..."

            )



    def on_chunk(
        self,
        chunk
    ):


        self.stream_buffer += chunk



        if self.current_ai_bubble:


            self.current_ai_bubble.set_text(

                self.stream_buffer

            )



        self.scroll_bottom()




    def on_finished(
        self,
        response
    ):


        self.stream_buffer = response



        if self.current_ai_bubble:


            self.current_ai_bubble.set_text(

                response

            )



        # Save Athena response

        conversation_service.save_ai_message(

            "",

            response

        )



        self.scroll_bottom()


        self.input_box.setFocus()



        self.conversation_updated.emit()




    def on_error(
        self,
        error
    ):


        if self.current_ai_bubble:


            self.current_ai_bubble.set_text(

                f"⚠️ {error}"

            )


        self.scroll_bottom()


        self.input_box.setFocus()