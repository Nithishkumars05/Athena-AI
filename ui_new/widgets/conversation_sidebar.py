from collections import defaultdict

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QInputDialog,
    QMessageBox,
    QLineEdit,
    QLabel,
)

from PySide6.QtCore import (
    Signal,
    Qt,
)

from services.conversation_service import conversation_service
from utils.date_utils import group_from_date


class ConversationSidebar(QWidget):

    conversation_selected = Signal(str)

    conversation_deleted = Signal(str)

    def __init__(self):

        super().__init__()

        self.layout = QVBoxLayout(self)

        self.layout.setContentsMargins(
            10,
            10,
            10,
            10
        )

        # =============================
        # Search
        # =============================

        self.search_box = QLineEdit()

        self.search_box.setPlaceholderText(
            "Search conversations..."
        )

        self.search_box.textChanged.connect(
            self.search_conversations
        )

        self.layout.addWidget(
            self.search_box
        )

        # =============================
        # New Chat
        # =============================

        self.new_chat_btn = QPushButton(
            "+ New Chat"
        )

        self.new_chat_btn.clicked.connect(
            self.create_new_chat
        )

        self.layout.addWidget(
            self.new_chat_btn
        )

        # =============================
        # Conversation List
        # =============================

        self.chat_list = QListWidget()

        self.chat_list.setFocusPolicy(
            Qt.NoFocus
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

        self.layout.addWidget(
            self.chat_list
        )

        self.refresh()

        # =====================================================
    # Refresh
    # =====================================================

    def refresh(self):

        current_id = None

        current_item = self.chat_list.currentItem()

        if current_item:

            current_id = current_item.data(
                Qt.UserRole
            )

        self.chat_list.clear()

        conversations = (
            conversation_service.list_conversations()
        )

        groups = defaultdict(list)

        for conversation in conversations:

            if conversation.get(
                "archived",
                False
            ):
                continue

            section = group_from_date(
                conversation["updated_at"]
            )

            groups[section].append(
                conversation
            )

        order = [

            "Today",

            "Yesterday",

            "Previous 7 Days",

            "Previous 30 Days",

            "Older"

        ]

        for section in order:

            chats = groups.get(section)

            if not chats:

                continue

            header = QListWidgetItem(section)

            header.setFlags(
                Qt.NoItemFlags
            )

            header.setForeground(
                Qt.gray
            )

            self.chat_list.addItem(
                header
            )

            for conversation in chats:

                title = conversation["title"]

                if conversation.get(
                    "pinned",
                    False
                ):
                    title = "📌 " + title

                item = QListWidgetItem(
                    title
                )

                item.setData(
                    Qt.UserRole,
                    conversation["id"]
                )

                self.chat_list.addItem(
                    item
                )

                if conversation["id"] == current_id:

                    self.chat_list.setCurrentItem(
                        item
                    )

        active = (
            conversation_service
            .get_active_conversation()
        )

        if active:

            self.select_conversation(
                active.id
            )

        # =====================================================
    # Search
    # =====================================================

    def search_conversations(
        self,
        text
    ):

        if not text.strip():

            self.refresh()
            return

        self.chat_list.clear()

        results = (
            conversation_service.search_conversations(
                text
            )
        )

        for conversation in results:

            title = conversation["title"]

            if conversation.get(
                "pinned",
                False
            ):
                title = "📌 " + title

            item = QListWidgetItem(
                title
            )

            item.setData(
                Qt.UserRole,
                conversation["id"]
            )

            self.chat_list.addItem(
                item
            )


    # =====================================================
    # Context Menu
    # =====================================================

    def show_context_menu(
        self,
        position
    ):

        item = self.chat_list.itemAt(position)

        if not item:
            return

        conversation_id = item.data(
            Qt.UserRole
        )

        if conversation_id is None:
            return

        conversation = (
            conversation_service.store.load(
                conversation_id
            )
        )

        if conversation is None:
            return

        menu = QMenu(self)

        rename_action = menu.addAction(
            "✏ Rename"
        )

        if conversation.pinned:

            pin_action = menu.addAction(
                "📍 Unpin"
            )

        else:

            pin_action = menu.addAction(
                "📌 Pin"
            )

        delete_action = menu.addAction(
            "🗑 Delete"
        )

        action = menu.exec(
            self.chat_list.mapToGlobal(
                position
            )
        )

        if action == rename_action:

            self.rename_chat(item)

        elif action == pin_action:

            conversation.pinned = (
                not conversation.pinned
            )

            conversation_service.store.save(
                conversation
            )

            self.refresh()

        elif action == delete_action:

            self.delete_chat(item)


    # =====================================================
    # Rename
    # =====================================================

    def rename_chat(
        self,
        item
    ):

        conversation_id = item.data(
            Qt.UserRole
        )

        title, ok = QInputDialog.getText(

            self,

            "Rename Conversation",

            "Title:",

            text=item.text().replace(
                "📌 ",
                ""
            )

        )

        if ok and title.strip():

            conversation_service.rename_conversation(

                conversation_id,

                title.strip()

            )

            self.refresh()


    # =====================================================
    # Delete
    # =====================================================

    def delete_chat(
        self,
        item
    ):

        conversation_id = item.data(
            Qt.UserRole
        )

        reply = QMessageBox.question(

            self,

            "Delete Conversation",

            "Delete this conversation?"

        )

        if reply == QMessageBox.Yes:

            conversation_service.delete_conversation(
                conversation_id
            )

            self.conversation_deleted.emit(
                conversation_id
            )

            self.refresh()


    # =====================================================
    # New Chat
    # =====================================================

    def create_new_chat(self):

        conversation = (
            conversation_service.new_conversation()
        )

        self.refresh()

        self.select_conversation(
            conversation.id
        )

        self.conversation_selected.emit(
            conversation.id
        )


    # =====================================================
    # Select
    # =====================================================

    def select_conversation(
        self,
        conversation_id
    ):

        for i in range(
            self.chat_list.count()
        ):

            item = self.chat_list.item(i)

            if item.flags() == Qt.NoItemFlags:
                continue

            if item.data(
                Qt.UserRole
            ) == conversation_id:

                self.chat_list.setCurrentItem(
                    item
                )

                break


    # =====================================================
    # Click
    # =====================================================

    def on_chat_selected(
        self,
        item
    ):

        conversation_id = item.data(
            Qt.UserRole
        )

        if conversation_id is None:
            return

        self.conversation_selected.emit(
            conversation_id
        )