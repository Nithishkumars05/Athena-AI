"""
Athena AI - PDF Processor

Responsible only for extracting text from PDF files.
Does not communicate with AI models.
"""


class PdfProcessor:
    """Extracts content from PDF documents."""

    def extract(self, file_path: str) -> str:
        raise NotImplementedError("PDF extraction not implemented yet.")