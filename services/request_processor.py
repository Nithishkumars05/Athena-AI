"""
Athena AI - Request Processor

Coordinates request preparation before
sending it to an AI model.

Responsibilities:
- Inspect ChatRequest
- Extract file contents
- Select the appropriate PromptBuilder
- Return a processed request

Does NOT communicate with AI models.
"""

from dataclasses import dataclass
from pathlib import Path

from models.chat_request import ChatRequest

from services.file_service import file_service

from services.prompt_builders.chat_prompt_builder import (
    chat_prompt_builder,
)

from services.prompt_builders.document_prompt_builder import (
    document_prompt_builder,
)


@dataclass
class ProcessedRequest:
    """
    Final request passed to the ChatAgent.
    """

    user_name: str
    prompt: str


class RequestProcessor:

    def process(
        self,
        request: ChatRequest,
    ) -> ProcessedRequest:

        # ----------------------------------
        # Document Conversation
        # ----------------------------------

        if request.file_path:

            document_text = file_service.extract_file(
                request.file_path
            )

            prompt = document_prompt_builder.build(
                user_name=request.user_name,
                message=request.message,
                document_text=document_text,
                file_name=Path(request.file_path).name,
            )

        # ----------------------------------
        # Normal Conversation
        # ----------------------------------

        else:

            prompt = chat_prompt_builder.build(
                user_name=request.user_name,
                message=request.message,
            )

        return ProcessedRequest(
            user_name=request.user_name,
            prompt=prompt,
        )


request_processor = RequestProcessor()