from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QListWidgetItem,
)

from PySide6.QtCore import Signal, Qt

from services.conversation_service import conversation_service


class ConversationSidebar(QWidget):

    conversation_selected = Signal(str)


    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.new_chat_btn = QPushButton(
            "+ New Chat"
        )

        self.chat_list = QListWidget()


        self.layout.addWidget(
            self.new_chat_btn
        )

        self.layout.addWidget(
            self.chat_list
        )


        self.new_chat_btn.clicked.connect(
            self.create_new_chat
        )

        self.chat_list.itemClicked.connect(
            self.on_chat_selected
        )


        self.refresh()


    def refresh(self):

        self.chat_list.clear()

        conversations = (
            conversation_service.list_conversations()
        )


        for conversation in conversations:

            item = QListWidgetItem(
                conversation["title"]
            )

            item.setData(
                Qt.UserRole,
                conversation["id"]
            )

            self.chat_list.addItem(item)



    def create_new_chat(self):

        conversation = (
            conversation_service.new_conversation()
        )

        self.refresh()

        self.conversation_selected.emit(
            conversation.id
        )



    def on_chat_selected(self, item):

        conversation_id = item.data(
            Qt.UserRole
        )

        self.conversation_selected.emit(
            conversation_id
        )