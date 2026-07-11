from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QPushButton,
)
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from datetime import datetime

from PySide6.QtGui import QClipboard

from ui_new.widgets.markdown_widget import MarkdownWidget



class ChatBubble(QWidget):


    def __init__(
        self,
        text: str,
        is_user: bool
    ):

        super().__init__()


        self.is_user = is_user



        # =====================================
        # Main Layout
        # =====================================


        main_layout = QHBoxLayout(
            self
        )


        main_layout.setContentsMargins(
            15,
            5,
            15,
            5
        )



        self.bubble = QFrame()


        self.bubble.setMaximumWidth(
            750
        )


        bubble_layout = QVBoxLayout(
            self.bubble
        )


        bubble_layout.setContentsMargins(
            15,
            10,
            15,
            10
        )


        bubble_layout.setSpacing(
            6
        )



        # =====================================
        # Header
        # =====================================


        self.sender = QLabel(

            "You"
            if is_user
            else "🦉 Athena"

        )


        self.sender.setStyleSheet(
            """
            color:#AAAAAA;
            font-size:11px;
            font-weight:bold;
            """
        )



        bubble_layout.addWidget(
            self.sender
        )



        # =====================================
        # Message Body
        # =====================================


        if is_user:


            self.label = QLabel(
                text
            )


            self.label.setWordWrap(
                True
            )


            self.label.setTextInteractionFlags(
                Qt.TextSelectableByMouse
            )


        else:


            self.label = MarkdownWidget()


            self.label.set_markdown(
                text
            )



        bubble_layout.addWidget(
            self.label
        )



        # =====================================
        # Footer
        # =====================================


        footer = QHBoxLayout()



        self.time = QLabel(

            datetime.now()
            .strftime("%H:%M")

        )


        self.time.setStyleSheet(
            """
            color:#888888;
            font-size:10px;
            """
        )



        footer.addWidget(
            self.time
        )



        footer.addStretch()



        # Copy button

        self.copy_btn = QPushButton(
            "Copy"
        )


        self.copy_btn.setFixedHeight(
            22
        )


        self.copy_btn.setStyleSheet(
            """
            QPushButton{
                background:transparent;
                color:#AAAAAA;
                border:none;
                font-size:11px;
            }

            QPushButton:hover{
                color:white;
            }
            """
        )


        self.copy_btn.clicked.connect(
            self.copy_text
        )


        footer.addWidget(
            self.copy_btn
        )



        bubble_layout.addLayout(
            footer
        )



        # =====================================
        # Styling
        # =====================================


        if is_user:


            self.bubble.setStyleSheet(
                """
                QFrame{
                    background:#2B6FFF;
                    border-radius:18px;
                }

                QLabel{
                    color:white;
                    font-size:14px;
                }
                """
            )


            main_layout.addStretch()

            main_layout.addWidget(
                self.bubble
            )


        else:


            self.bubble.setStyleSheet(
                """
                QFrame{
                    background:#303030;
                    border-radius:18px;
                }

                QLabel{
                    color:white;
                    font-size:14px;
                }
                """
            )


            main_layout.addWidget(
                self.bubble
            )

            main_layout.addStretch()



    # =====================================
    # Update Streaming Text
    # =====================================


    def set_text(
        self,
        text: str
    ):


        if self.is_user:


            self.label.setText(
                text
            )


        else:


            self.label.set_markdown(
                text
            )



        self.bubble.adjustSize()

        self.adjustSize()

        self.updateGeometry()



    # =====================================
    # Copy
    # =====================================


    def copy_text(self):


        if self.is_user:


            text = self.label.text()


        else:


            try:

                text = self.label.toPlainText()

            except:

                text = ""



        clipboard = (
            QApplication
            .clipboard()
        )


        clipboard.setText(
            text
        )