from PySide6.QtCore import QRunnable, Slot, Signal, QObject
from agents.chat_agent import chat
import traceback


class WorkerSignals(QObject):
    finished = Signal(str)
    error = Signal(str)


class ChatWorker(QRunnable):

    def __init__(self, message: str):
        super().__init__()
        self.message = message
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            response = chat("User", self.message)
            self.signals.finished.emit(response)

        except Exception:
            error = traceback.format_exc()
            print(error)
            self.signals.error.emit(error)