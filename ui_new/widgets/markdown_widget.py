from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtGui import QTextDocument, QPainter
from PySide6.QtCore import Qt, QSize


class MarkdownWidget(QWidget):
    """
    Lightweight markdown renderer.

    Unlike QTextBrowser:
    - no scrollbars
    - auto expands
    - paints directly
    - ideal for chat bubbles
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.document = QTextDocument(self)

        self.document.setDocumentMargin(0)

        self.document.setMarkdown("")

        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

    # --------------------------------------------------

    def set_markdown(self, text: str):

        self.document.setMarkdown(text)

        self.document.adjustSize()

        self.updateGeometry()

        self.update()

    # --------------------------------------------------

    def sizeHint(self):

        size = self.document.size()

        return QSize(
            self.width(),
            int(size.height())
        )

    # --------------------------------------------------

    def minimumSizeHint(self):

        return self.sizeHint()

    # --------------------------------------------------

    def paintEvent(self, event):

        painter = QPainter(self)

        self.document.setTextWidth(
            self.width()
        )

        self.document.drawContents(
            painter,
    self.rect()
        )

        painter.end()

    # --------------------------------------------------

    def heightForWidth(self, width):

        self.document.setTextWidth(width)

        self.document.adjustSize()

        return int(
            self.document.size().height()
        )