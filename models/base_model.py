"""
Athena AI - Base Model Interface

Defines the common interface for all AI providers.

Supports:
- Text generation
- Streaming generation
- Optional image input for vision models
"""

from abc import ABC, abstractmethod


class BaseModel(ABC):

    @abstractmethod
    def generate(
        self,
        user_name: str,
        prompt: str,
        original_message: str | None = None,
        image_path: str | None = None,
    ) -> str:
        """
        Generate a complete response.
        """
        pass


    @abstractmethod
    def stream_generate(
        self,
        user_name: str,
        prompt: str,
        original_message: str | None = None,
        image_path: str | None = None,
    ):
        """
        Yield response chunks.
        """
        pass