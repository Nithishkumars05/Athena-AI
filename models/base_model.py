from abc import ABC, abstractmethod


class BaseModel(ABC):

    @abstractmethod
    def generate(self, user_name: str, message: str) -> str:
        """
        Generate a complete response.
        """
        pass


    @abstractmethod
    def stream_generate(self, user_name: str, message: str):
        """
        Yield response chunks.

        Example:

        Hello
        Hello there
        Hello there!
        """
        pass