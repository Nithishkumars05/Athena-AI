"""
Athena AI - DOCX Processor

Responsible only for extracting text from DOCX files.
Does not communicate with AI models.
"""


class DocxProcessor:
    """Extracts content from DOCX documents."""

    def extract(self, file_path: str) -> str:
        raise NotImplementedError("DOCX extraction not implemented yet.")