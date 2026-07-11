from PySide6.QtWidgets import (
    QWidget,
    QSplitter,
    QHBoxLayout
)
from PySide6.QtCore import Qt
from ui_new.widgets.ai_conversation import AIConversationWidget
from ui_new.widgets.conversation_sidebar import ConversationSidebar


class ChatPage(QWidget):

    def __init__(self):

        super().__init__()

        layout = QHBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)

        self.sidebar = ConversationSidebar()
        self.sidebar.setMinimumWidth(220)
        self.sidebar.setMaximumWidth(450)

        self.chat = AIConversationWidget(
        mode="chat"
    )

        splitter = QSplitter(Qt.Horizontal)

        splitter.addWidget(self.sidebar)

        splitter.addWidget(self.chat)

    # Initial sizes
        splitter.setSizes([
        260,
        1200
    ])

    # Chat gets remaining space
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        layout.addWidget(splitter)

        self.sidebar.conversation_selected.connect(
            self.switch_conversation
    )

        self.chat.conversation_updated.connect(
            self.refresh_sidebar
    )

    def refresh_sidebar(self):

        self.sidebar.refresh()

    def switch_conversation(
        self,
        conversation_id
    ):

        from services.conversation_service import conversation_service

        conversation_service.switch_conversation(
            conversation_id
        )

        self.chat.reload_messages()