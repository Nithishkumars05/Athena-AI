from abc import ABC, abstractmethod


class BaseModel(ABC):

    @abstractmethod
    def generate(self, user_name: str, message: str) -> str:
        """
        Generate a response from the AI model.
        """
        pass