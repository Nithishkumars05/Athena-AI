from PySide6.QtWidgets import QWidget, QVBoxLayout
from ui_new.widgets.ai_conversation import AIConversationWidget


class ChatPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(
            AIConversationWidget(mode="chat")
        )