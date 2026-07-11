from PySide6.QtCore import QObject, QRunnable, Signal, Slot

from agents.dispatcher import dispatcher
from models.chat_request import ChatRequest
from core.logger import logger
import traceback


class WorkerSignals(QObject):
    started = Signal()
    chunk_received = Signal(str)
    finished = Signal(str)
    error = Signal(str)


class ChatWorker(QRunnable):

    def __init__(
        self,
        request: ChatRequest,
        streaming: bool = False,
    ):
        super().__init__()

        self.request = request
        self.streaming = streaming
        self.signals = WorkerSignals()

    @Slot()
    @Slot()
    def run(self):

        self.signals.started.emit()

        try:

            logger.info("Chat request started")

            if self.streaming:

                response = ""

                for chunk in dispatcher.stream_handle(self.request):

                    response += chunk

                    self.signals.chunk_received.emit(
                    chunk
                )

                logger.info(
                "Streaming chat completed"
            )

                self.signals.finished.emit(
                response
            )

            else:

                response = dispatcher.handle(
                self.request
            )

                logger.info(
                "Chat request completed"
            )

                self.signals.finished.emit(
                response
            )


        except Exception as e:

            logger.exception(
            "Chat request failed"
        )

            self.signals.error.emit(
            str(e)
        )