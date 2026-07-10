"""
Athena AI - Request Processor

Coordinates request preparation before
sending it to an AI model.

Responsibilities:
- Inspect ChatRequest
- Extract file contents
- Select appropriate PromptBuilder
- Return processed request

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


IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
}


@dataclass
class ProcessedRequest:
    """
    Final request passed to the ChatAgent.
    """

    user_name: str
    original_message: str
    prompt: str
    file_path: str | None = None
    file_type: str | None = None

class RequestProcessor:

    def process(
        self,
        request: ChatRequest,
    ) -> ProcessedRequest:

        # ----------------------------------
        # File Conversation
        # ----------------------------------

        if request.file_path:

            extension = Path(
                request.file_path
            ).suffix.lower()


            # ------------------------------
            # Image File
            # ------------------------------

            if extension in IMAGE_EXTENSIONS:

                image_data = file_service.extract_file(
                    request.file_path
                )

                print("=" * 60)
                print("IMAGE DATA:")
                print(image_data)
                print("=" * 60)


                prompt = chat_prompt_builder.build(
                    user_name=request.user_name,
                    message=request.message,
                )


            # ------------------------------
            # Document File
            # ------------------------------

            else:

                document_text = file_service.extract_file(
                    request.file_path
                )

                print("=" * 60)
                print("DOCUMENT LENGTH:",
                      len(document_text))

                print("FIRST 500 CHARACTERS:")
                print(document_text[:500])
                print("=" * 60)


                prompt = document_prompt_builder.build(
                    user_name=request.user_name,
                    message=request.message,
                    document_text=document_text,
                    file_name=Path(
                        request.file_path
                    ).name,
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
            original_message=request.message,
            prompt=prompt,
            file_path=request.file_path,
    file_type=(
        "image"
        if request.file_path
        and Path(request.file_path).suffix.lower()
        in IMAGE_EXTENSIONS
        else None
    ),
        )


request_processor = RequestProcessor()