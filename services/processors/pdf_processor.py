"""
Athena AI - PDF Processor

Responsible for extracting text from PDF documents.

Does NOT communicate with AI models.
"""

from pypdf import PdfReader


class PdfProcessor:
    """Extracts text from PDF documents."""

    def extract(self, file_path: str) -> str:
        """
        Read every page of a PDF and return the extracted text.
        """
        reader = PdfReader(file_path)

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n".join(pages)