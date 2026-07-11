from PySide6.QtWidgets import QTextEdit
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QKeyEvent


class MessageInput(QTextEdit):
    """
    ChatGPT-style message input.

    Features:
    - Enter = Send
    - Shift+Enter = New Line
    - Auto growing
    """

    sendRequested = Signal()

    def __init__(self):
        super().__init__()
        self.setFocusPolicy(Qt.StrongFocus)
        self.setPlaceholderText("Message Athena...")

        self.setMinimumHeight(45)
        self.setMaximumHeight(140)

        self.textChanged.connect(
            self.auto_resize
        )

        self.setStyleSheet("""
        QTextEdit{
            border:none;
            background:transparent;
            color:white;
            font-size:14px;
            padding:4px;
        }
        """)

    # ---------------------------------
    # Auto Resize
    # ---------------------------------

    def auto_resize(self):

        document_height = (
            self.document()
            .size()
            .height()
        )

        height = int(document_height) + 14

        if height < 45:
            height = 45

        if height > 140:
            height = 140

        self.setFixedHeight(height)

    # ---------------------------------
    # Keyboard
    # ---------------------------------

    def keyPressEvent(
        self,
        event: QKeyEvent
    ):

        if (
            event.key() in (
                Qt.Key_Return,
                Qt.Key_Enter
            )
            and not (
                event.modifiers()
                & Qt.ShiftModifier
            )
        ):

            self.sendRequested.emit()
            return

        super().keyPressEvent(event)