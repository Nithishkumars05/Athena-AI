from PySide6.QtCore import QThreadPool

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
    ):


        request = ChatRequest(
    user_name="User",
    message=message,
    file_path=file_path,
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
    ):


        request = ChatRequest(
    user_name="User",
    message=message,
    file_path=file_path,
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