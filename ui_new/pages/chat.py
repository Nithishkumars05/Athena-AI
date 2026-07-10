from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout
)

from ui_new.widgets.ai_conversation import AIConversationWidget
from ui_new.widgets.conversation_sidebar import ConversationSidebar


class ChatPage(QWidget):

    def __init__(self):

        super().__init__()


        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            0,0,0,0
        )


        self.sidebar = ConversationSidebar()

        self.chat = AIConversationWidget(
            mode="chat"
        )


        layout.addWidget(
            self.sidebar
        )

        layout.addWidget(
            self.chat
        )


        self.sidebar.conversation_selected.connect(
            self.switch_conversation
        )



    def switch_conversation(
        self,
        conversation_id
    ):

        from services.conversation_service import conversation_service

        conversation_service.switch_conversation(
            conversation_id
        )

        self.chat.reload_messages()