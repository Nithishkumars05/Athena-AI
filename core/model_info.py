from dataclasses import dataclass

from models.base_model import BaseModel


@dataclass
class ModelInfo:
    """
    Metadata about an AI model.
    """

    name: str
    provider: str      # "cloud" or "offline"
    instance: BaseModel