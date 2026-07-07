from PySide6.QtCore import QThreadPool
from services.workers.chat_worker import ChatWorker


class ChatService:

    def __init__(self):
        self.threadpool = QThreadPool.globalInstance()

    def send_message(self, message, callback, error_callback=None):
        worker = ChatWorker(message)

        worker.signals.finished.connect(callback)

        if error_callback:
            worker.signals.error.connect(error_callback)

        self.threadpool.start(worker)


chat_service = ChatService()