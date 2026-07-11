from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QInputDialog,
    QMessageBox,
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
        self.new_chat_btn.setFocusPolicy(
    Qt.NoFocus
)

        self.chat_list = QListWidget()
        self.chat_list.setFocusPolicy(
    Qt.NoFocus
)


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
        self.chat_list.setContextMenuPolicy(
        Qt.CustomContextMenu
)

        self.chat_list.customContextMenuRequested.connect(
    self.show_context_menu
)

        self.refresh()
    def show_context_menu(self, position):

        item = self.chat_list.itemAt(position)

        if not item:
            return


        menu = QMenu()


        rename_action = menu.addAction(
            "Rename"
    )
        delete_action = menu.addAction(
            "Delete"
)


        action = menu.exec(
            self.chat_list.mapToGlobal(position)
    )


        if action == rename_action:

            self.rename_chat(item)

        elif action == delete_action:

            self.delete_chat(item)

    def rename_chat(self, item):

        conversation_id = item.data(
        Qt.UserRole
    )

        print("Renaming ID:", conversation_id)

        new_title, ok = QInputDialog.getText(
        self,
        "Rename Conversation",
        "Title:"
    )

        if ok and new_title.strip():

            print("New title:", new_title)

            result = conversation_service.rename_conversation(
            conversation_id,
            new_title.strip()
        )

            print(
            "Returned title:",
            result.title if result else None
        )

            print(
            "After save:",
            conversation_service.list_conversations()
        )

            self.refresh()

    def delete_chat(self, item):

        conversation_id = item.data(
        Qt.UserRole
    )


        reply = QMessageBox.question(
        self,
        "Delete Conversation",
        "Are you sure you want to delete this conversation?"
    )


        if reply == QMessageBox.Yes:

            conversation_service.delete_conversation(
            conversation_id
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