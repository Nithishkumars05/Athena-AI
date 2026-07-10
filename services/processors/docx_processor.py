"""
Athena AI - DOCX Processor

Responsible for extracting text from Microsoft Word
documents.

Does NOT communicate with AI models.
"""

from docx import Document


class DocxProcessor:
    """Extracts text from DOCX documents."""

    def extract(self, file_path: str) -> str:
        """
        Read all paragraphs from a DOCX file and return
        them as plain text.
        """
        document = Document(file_path)

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n".join(paragraphs)