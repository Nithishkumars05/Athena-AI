from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFrame,
)
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPushButton, QHBoxLayout

class AttachmentPreview(QFrame):
    removed = Signal()
    """
    Displays a preview of an attached file.

    Currently supports:
    - Images

    Future:
    - PDF
    - DOCX
    - TXT
    - Code
    """

    IMAGE_EXTENSIONS = {
        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".gif",
        ".webp",
    }

    def __init__(self, file_path: str):
        super().__init__()

        self.file_path = file_path

        self.setStyleSheet("""
        QFrame{
            background:#3A3A3A;
            border-radius:12px;
        }

        QLabel{
            color:white;
        }
        """)

        layout = QVBoxLayout(self)
        top = QHBoxLayout()

        top.addStretch()

        close_btn = QPushButton("✕")

        close_btn.setFixedSize(24, 24)

        close_btn.clicked.connect(
    self.removed.emit
)

        close_btn.setStyleSheet("""
QPushButton{
    background:#555555;
    border:none;
    border-radius:12px;
    color:white;
}

QPushButton:hover{
    background:#D9534F;
}
""")

        top.addWidget(close_btn)

        layout.addLayout(top)
        layout.setContentsMargins(10, 10, 10, 10)

        extension = Path(file_path).suffix.lower()

        if extension in self.IMAGE_EXTENSIONS:

            image = QLabel()

            pixmap = QPixmap(file_path)

            if not pixmap.isNull():

                pixmap = pixmap.scaled(
                    250,
                    250,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation,
                )

                image.setPixmap(pixmap)

            layout.addWidget(image)

        filename = QLabel(Path(file_path).name)

        filename.setStyleSheet("""
        font-weight:bold;
        """)

        layout.addWidget(filename)