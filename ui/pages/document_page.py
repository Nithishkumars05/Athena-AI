from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QTextBrowser, QLabel, QFileDialog
)
from PySide6.QtCore import Qt

from agents.document_agent import summarize_document


class DocumentPage(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        # Title
        title = QLabel("Document Analyzer")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:22px; font-weight:bold;")

        # Button
        self.select_button = QPushButton("Select File & Summarize")
        self.select_button.clicked.connect(self.select_file)

        # Output
        self.output_box = QTextBrowser()

        self.layout.addWidget(title)
        self.layout.addWidget(self.select_button)
        self.layout.addWidget(self.output_box)

        self.setLayout(self.layout)

    def select_file(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Document",
            "",
            "Documents (*.pdf *.docx *.txt)"
        )

        if not file_path:
            return

        self.output_box.append(f"Reading file: {file_path}\n")

        try:
            summary = summarize_document("User", file_path)

            self.output_box.append("Summary:\n")
            self.output_box.append(summary)
            self.output_box.append("-" * 40)

        except Exception as e:
            self.output_box.append(f"Error: {str(e)}")