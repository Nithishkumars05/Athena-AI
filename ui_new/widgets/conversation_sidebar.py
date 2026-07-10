from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QListWidget,
)

from PySide6.QtCore import Signal

from services.conversation_service import conversation_service


class ConversationSidebar(QWidget):

    conversation_selected = Signal(str)

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.new_chat_btn = QPushButton(
            "+ New Chat"
        )

        self.list_widget = QListWidget()


        self.layout.addWidget(
            self.new_chat_btn
        )

        self.layout.addWidget(
            self.list_widget
        )


        self.new_chat_btn.clicked.connect(
            self.new_chat
        )

        self.list_widget.itemClicked.connect(
            self.select_conversation
        )


        self.refresh()


    def refresh(self):

        self.list_widget.clear()

        conversations = (
            conversation_service.list_conversations()
        )

        for conv in conversations:

            self.list_widget.addItem(
                conv["title"]
            )


    def new_chat(self):

        conversation = (
            conversation_service.new_conversation()
        )

        self.refresh()


    def select_conversation(self, item):

        conversations = (
            conversation_service.list_conversations()
        )

        index = self.list_widget.row(item)

        conversation_id = conversations[index]["id"]

        self.conversation_selected.emit(
            conversation_id
        )