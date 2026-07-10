"""
Athena AI - Code Processor

Responsible for extracting source code from supported
programming language files.

Does NOT perform analysis.
Does NOT communicate with AI models.
"""


class CodeProcessor:
    """Extracts source code from code files."""

    def extract(self, file_path: str) -> str:
        """
        Read and return the contents of a source code file.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()