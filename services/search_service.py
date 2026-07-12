"""
Athena AI

Search Service

Responsibilities
----------------
- Manage search providers
- Route search requests
- Return normalized results

This service DOES NOT:
- Contain UI
- Talk directly to AI models
- Perform intent detection

Providers:
- DuckDuckGo (planned)
- Tavily (planned)
- Brave (planned)
- SerpAPI (planned)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional


# ==========================================================
# Search Result
# ==========================================================

@dataclass
class SearchResult:

    title: str

    url: str

    snippet: str

    source: str = ""


# ==========================================================
# Provider Interface
# ==========================================================

class SearchProvider(ABC):

    @abstractmethod
    def search(
        self,
        query: str,
        max_results: int = 5
    ) -> List[SearchResult]:
        """
        Execute a search.
        """
        raise NotImplementedError


# ==========================================================
# Search Service
# ==========================================================

class SearchService:

    def __init__(self):

        self.providers: Dict[str, SearchProvider] = {}

        self.default_provider: Optional[str] = None

    # ------------------------------------------------------

    def register_provider(
        self,
        name: str,
        provider: SearchProvider
    ):

        self.providers[name] = provider

        if self.default_provider is None:
            self.default_provider = name

    # ------------------------------------------------------

    def set_default_provider(
        self,
        name: str
    ):

        if name not in self.providers:

            raise ValueError(
                f"Unknown provider: {name}"
            )

        self.default_provider = name

    # ------------------------------------------------------

    def search(
        self,
        query: str,
        max_results: int = 5
    ) -> List[SearchResult]:

        if self.default_provider is None:

            raise RuntimeError(
                "No search provider registered."
            )

        provider = self.providers[
            self.default_provider
        ]

        return provider.search(
            query=query,
            max_results=max_results
        )


search_service = SearchService()
from services.search_providers import DuckDuckGoProvider

search_service.register_provider(
    "duckduckgo",
    DuckDuckGoProvider()
)