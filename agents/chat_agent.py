"""
Athena AI - Chat Agent

The Chat Agent acts as a coordinator.
It does not know which AI model is being used.

Flow:
UI
 ↓
ChatService
 ↓
ChatWorker
 ↓
ChatAgent
 ↓
ModelManager
 ↓
Gemini / Ollama
"""

from models.chat_request import ChatRequest

from core.model_manager import model_manager
from core.routers.task_router import task_router
from core.routers.model_router import model_router


def chat(request: ChatRequest) -> str:
    """
    Handle a standard chat request.
    """

    task_type = task_router.classify(request.message)

    model_name = model_router.select_model(
        task_type
    )

    return model_manager.generate_with_model(
        model_name=model_name,
        user_name=request.user_name,
        message=request.message
    )


def handle(request: ChatRequest) -> str:
    return chat(request)


def stream(request: ChatRequest):
    """
    Handle a streaming chat request.
    """

    task_type = task_router.classify(request.message)

    model_name = model_router.select_model(
        task_type
    )

    yield from model_manager.stream_generate_with_model(
        model_name=model_name,
        user_name=request.user_name,
        message=request.message
    )


def stream_handle(request: ChatRequest):
    yield from stream(request)