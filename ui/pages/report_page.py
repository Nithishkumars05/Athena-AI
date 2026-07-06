from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QTextBrowser, QLabel
)
from PySide6.QtCore import Qt

from agents.chat_agent import chat
from agents.report_agent import create_report


class ReportPage(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        # Title
        title = QLabel("Report Generator")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:22px; font-weight:bold;")

        # Input
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Enter report topic...")

        # Button
        self.generate_button = QPushButton("Generate Report")
        self.generate_button.clicked.connect(self.generate_report)

        # Output
        self.output_box = QTextBrowser()

        self.layout.addWidget(title)
        self.layout.addWidget(self.input_box)
        self.layout.addWidget(self.generate_button)
        self.layout.addWidget(self.output_box)

        self.setLayout(self.layout)

    def generate_report(self):

        topic = self.input_box.text().strip()

        if not topic:
            return

        self.output_box.append(f"Generating report for: {topic}\n")

        try:
            prompt = f"""
Write a detailed structured report on:

{topic}

Include:
1. Introduction
2. Explanation
3. Advantages
4. Disadvantages
5. Applications
6. Conclusion
"""

            report = chat("User", prompt)

            filename = create_report(topic, report)

            self.output_box.append("Report Generated Successfully ✔")
            self.output_box.append(f"Saved as: {filename}")
            self.output_box.append("-" * 40)

        except Exception as e:
            self.output_box.append(f"Error: {str(e)}")