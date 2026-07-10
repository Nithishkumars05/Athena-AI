"""
Athena AI - TXT Processor

Responsible only for extracting text from TXT files.
Does not communicate with AI models.
"""


class TxtProcessor:
    """Extracts content from text files."""

    def extract(self, file_path: str) -> str:
        """
        Read and return the contents of a text file.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()