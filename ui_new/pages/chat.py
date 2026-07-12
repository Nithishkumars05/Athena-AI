from PySide6.QtWidgets import (
    QWidget,
    QSplitter,
    QHBoxLayout,
)

from PySide6.QtCore import Qt

from ui_new.widgets.ai_conversation import AIConversationWidget
from ui_new.widgets.conversation_sidebar import ConversationSidebar

from services.conversation_service import conversation_service



class ChatPage(QWidget):


    def __init__(self):

        super().__init__()



        # =====================================
        # Layout
        # =====================================


        layout = QHBoxLayout(
            self
        )


        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )



        # =====================================
        # Sidebar
        # =====================================


        self.sidebar = ConversationSidebar()


        self.sidebar.setMinimumWidth(
            220
        )


        self.sidebar.setMaximumWidth(
            450
        )



        # =====================================
        # Chat
        # =====================================


        self.chat = AIConversationWidget(

            mode="chat"

        )



        # =====================================
        # Splitter
        # =====================================


        splitter = QSplitter(
            Qt.Horizontal
        )


        splitter.addWidget(
            self.sidebar
        )


        splitter.addWidget(
            self.chat
        )


        splitter.setSizes(
            [
                260,
                1200
            ]
        )


        splitter.setStretchFactor(
            0,
            0
        )


        splitter.setStretchFactor(
            1,
            1
        )


        layout.addWidget(
            splitter
        )



        # =====================================
        # Signals
        # =====================================


        self.sidebar.conversation_selected.connect(

            self.switch_conversation

        )


        self.sidebar.conversation_deleted.connect(

            self.refresh_sidebar

        )


        self.chat.conversation_updated.connect(

            self.refresh_sidebar

        )



        # Initial header

        self.update_header()




    # =====================================
    # Sidebar Refresh
    # =====================================


    def refresh_sidebar(self):


        self.sidebar.refresh()


        self.update_header()




    # =====================================
    # Switch Conversation
    # =====================================


    def switch_conversation(
        self,
        conversation_id
    ):


        conversation = (
            conversation_service
            .switch_conversation(
                conversation_id
            )
        )


        if conversation:


            self.chat.reload_messages()


            self.update_header()




    # =====================================
    # Header Sync
    # =====================================


    def update_header(self):


        conversation = (
            conversation_service
            .get_active_conversation()
        )


        if not conversation:

            return



        self.chat.header.set_title(

            f"💬 {conversation.title}"

        )


        self.chat.header.set_subtitle(

            "General AI conversation"

        )