from PySide6.QtCore import QThreadPool
from core.logger import logger
from models.chat_request import ChatRequest
from services.workers.chat_worker import ChatWorker
from models.chat_request import ChatRequest

class ChatService:

    def __init__(self):
        self.threadpool = QThreadPool.globalInstance()

    # -------------------------
    # Normal Request
    # -------------------------

    def send_message(
        self,
        message,
        callback,
        error_callback=None,
        file_path=None,
        user_name="User",
        conversation_id=None,
    ):


        request = ChatRequest(
    user_name=user_name,
    message=message,
    file_path=file_path,
    conversation_id=conversation_id,
)
        logger.info(
    f"Request received | "
    f"User={user_name} | "
    f"Streaming=False | "
    f"File={file_path is not None}"
)

        worker = ChatWorker(
    request,
    streaming=False,
)

        worker.signals.finished.connect(callback)

        if error_callback:
            worker.signals.error.connect(error_callback)

        self.threadpool.start(worker)

    # -------------------------
    # Streaming Request
    # -------------------------

    def stream_message(
        self,
        message,
        chunk_callback,
        finished_callback,
        error_callback=None,
        started_callback=None,
        file_path=None,
        user_name="User",
        conversation_id=None,
    ):


        request = ChatRequest(
    user_name=user_name,
    message=message,
    file_path=file_path,
    conversation_id=conversation_id,

)
        logger.info(
    f"Request received | "
    f"User={user_name} | "
    f"Streaming=True | "
    f"File={file_path is not None}"
)

        worker = ChatWorker(
    request,
    streaming=True,
)

        if started_callback:
            worker.signals.started.connect(started_callback)

        worker.signals.chunk_received.connect(chunk_callback)

        worker.signals.finished.connect(finished_callback)

        if error_callback:
            worker.signals.error.connect(error_callback)

        self.threadpool.start(worker)


chat_service = ChatService()