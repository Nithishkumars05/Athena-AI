"""
Athena AI - Code Processor

Responsible only for extracting source code files.
Does not communicate with AI models.
"""


class CodeProcessor:
    """Extracts content from source code files."""

    def extract(self, file_path: str) -> str:
        raise NotImplementedError("Code extraction not implemented yet.")