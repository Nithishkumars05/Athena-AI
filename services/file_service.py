"""
Athena AI - File Service

Orchestrates file extraction.

Responsibilities:
- Validate uploaded files
- Select the appropriate processor
- Delegate extraction

This service never communicates with AI models.
"""

from pathlib import Path

from services.processors.pdf_processor import PdfProcessor
from services.processors.docx_processor import DocxProcessor
from services.processors.txt_processor import TxtProcessor
from services.processors.image_processor import ImageProcessor
from services.processors.code_processor import CodeProcessor


class FileService:
    """
    Coordinates document processing.

    UI -> FileService -> Processor
    """

    def __init__(self):
        self._processors = {
            ".pdf": PdfProcessor(),
            ".docx": DocxProcessor(),
            ".txt": TxtProcessor(),

            ".py": CodeProcessor(),
            ".cpp": CodeProcessor(),
            ".c": CodeProcessor(),
            ".h": CodeProcessor(),
            ".hpp": CodeProcessor(),
            ".java": CodeProcessor(),
            ".js": CodeProcessor(),
            ".ts": CodeProcessor(),
            ".py": CodeProcessor(),
".cpp": CodeProcessor(),
".c": CodeProcessor(),
".h": CodeProcessor(),
".hpp": CodeProcessor(),
".java": CodeProcessor(),
".js": CodeProcessor(),
".ts": CodeProcessor(),
".cs": CodeProcessor(),
".go": CodeProcessor(),
".rs": CodeProcessor(),
".php": CodeProcessor(),
".html": CodeProcessor(),
".css": CodeProcessor(),
".json": CodeProcessor(),
".xml": CodeProcessor(),
".yaml": CodeProcessor(),
".yml": CodeProcessor(),
".toml": CodeProcessor(),
            ".png": ImageProcessor(),
            ".jpg": ImageProcessor(),
            ".jpeg": ImageProcessor(),
            ".bmp": ImageProcessor(),
        }

    def extract_file(self, file_path: str) -> str:
        self._validate(file_path)

        extension = Path(file_path).suffix.lower()
        processor = self._get_processor(extension)

        return processor.extract(file_path)

    def _validate(self, file_path: str):
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(file_path)

        if not path.is_file():
            raise ValueError("The provided path is not a file.")

    def _get_processor(self, extension: str):
        processor = self._processors.get(extension)

        if processor is None:
            raise ValueError(f"Unsupported file type: {extension}")

        return processor
file_service = FileService()