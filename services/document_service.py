"""
Athena AI - Document Service

Coordinates document processing.

Responsibilities:
- Extract document text
- Build document prompts

Does NOT communicate with AI models.
"""

from pathlib import Path

from services.file_service import file_service
from services.conversation_service import conversation_service


class DocumentService:
    """
    Orchestrates document-based conversations.
    """

    def build_prompt(
        self,
        user_name: str,
        message: str,
        file_path: str,
    ) -> str:

        document_text = file_service.extract_file(file_path)

        return conversation_service.build_document_prompt(
            user_name=user_name,
            message=message,
            document_text=document_text,
            file_name=Path(file_path).name,
        )


document_service = DocumentService()