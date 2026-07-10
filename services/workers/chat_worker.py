from PySide6.QtCore import QObject, QRunnable, Signal, Slot

from agents.dispatcher import dispatcher
from models.chat_request import ChatRequest

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
    def run(self):

        try:
            self.signals.started.emit()

            # -----------------------------
            # Streaming Mode
            # -----------------------------
            if self.streaming:

                full_response = ""

                for chunk in dispatcher.stream_handle(
                    self.request
                ):
                    full_response += chunk
                    self.signals.chunk_received.emit(chunk)

                self.signals.finished.emit(full_response)

            # -----------------------------
            # Normal Mode
            # -----------------------------
            else:

                response = dispatcher.handle(
                    self.request
                )

                self.signals.finished.emit(response)

        except Exception:

            error = traceback.format_exc()

            print(error)

            self.signals.error.emit(error)