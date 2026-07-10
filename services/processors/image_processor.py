"""
Athena AI - Image Processor

Responsible only for extracting information from images.
Does not communicate with AI models.
"""


class ImageProcessor:
    """Extracts content from image files."""

    def extract(self, file_path: str) -> str:
        raise NotImplementedError("Image extraction not implemented yet.")