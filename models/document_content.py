"""
Athena AI - Document Content

Represents extracted content from any supported file.
"""

from dataclasses import dataclass, field


@dataclass
class DocumentContent:
    text: str
    file_name: str
    file_type: str
    metadata: dict = field(default_factory=dict)