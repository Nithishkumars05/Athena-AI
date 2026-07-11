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
from core.conversation_manager import conversation_manager
from memory.conversation_memory import conversation_memory

def chat(request: ChatRequest) -> str:

    processed = request_processor.process(request)

    task_type = task_router.classify(
        processed
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

    # Create a conversation if this is a new chat
    if request.conversation_id is None:
        conversation = conversation_manager.new_conversation()
        request.conversation_id = conversation.id
    else:
        conversation_manager.set_current(request.conversation_id)

    # Save the user's message
    conversation_manager.add_message(
        role="user",
        content=request.message,
        conversation_id=request.conversation_id,
    )

    # Generate the response
    response = chat(request)

    # Save the assistant's reply
    conversation_manager.add_message(
        role="assistant",
        content=response,
        conversation_id=request.conversation_id,
    )

    # Persist to disk
    conversation = conversation_manager.get_conversation(
        request.conversation_id
)

    conversation_memory.save(conversation)

    return response


def stream(request: ChatRequest):

    processed = request_processor.process(request)

    task_type = task_router.classify(
        processed
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