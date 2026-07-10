"""
Athena AI - Chat Agent

Coordinates the request pipeline.

Flow:

ChatRequest
    ↓
RequestProcessor
    ↓
TaskRouter
    ↓
ModelRouter
    ↓
ModelManager
"""

from models.chat_request import ChatRequest

from services.request_processor import request_processor

from core.model_manager import model_manager
from core.routers.task_router import task_router
from core.routers.model_router import model_router


def chat(request: ChatRequest) -> str:

    processed = request_processor.process(request)

    task_type = task_router.classify(
        request.message
    )

    model_name = model_router.select_model(
        task_type
    )

    return model_manager.generate_with_model(
        model_name=model_name,
        user_name=processed.user_name,
        prompt=processed.prompt,
        original_message=processed.original_message,
        image_path=processed.file_path,
    )


def handle(request: ChatRequest) -> str:

    return chat(request)


def stream(request: ChatRequest):

    processed = request_processor.process(request)

    task_type = task_router.classify(
        request.message
    )

    model_name = model_router.select_model(
        task_type
    )

    yield from model_manager.stream_generate_with_model(
        model_name=model_name,
        user_name=processed.user_name,
        prompt=processed.prompt,
        original_message=processed.original_message,
        image_path=processed.file_path,
    )


def stream_handle(request: ChatRequest):

    yield from stream(request)