from dataclasses import dataclass

from models.base_model import BaseModel


@dataclass
class ModelInfo:
    """
    Metadata describing an AI model.
    """

    # Internal model name
    name: str

    # Display name for UI
    display_name: str

    # cloud | offline
    provider: str

    # chat | coding | reasoning | vision
    capabilities: list[str]

    # Short description
    description: str

    # Capabilities
    supports_streaming: bool
    supports_vision: bool

    # Recommended use
    recommended_for: list[str]
    # Actual model instance
    instance: BaseModel