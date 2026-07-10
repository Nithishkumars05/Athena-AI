"""
Athena AI - Image Processor

Responsible only for preparing image files
for vision processing.

Does NOT communicate with AI models.
"""

from pathlib import Path


class ImageProcessor:
    """Processes image file information."""

    def extract(self, file_path: str) -> dict:
        """
        Return image metadata required
        for vision processing.
        """

        path = Path(file_path)

        return {
            "type": "image",
            "path": str(path),
            "extension": path.suffix.lower(),
        }