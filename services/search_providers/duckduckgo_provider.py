"""
Athena AI

DDGS Search Provider
"""

from ddgs import DDGS

from services.search_service import (
    SearchProvider,
    SearchResult,
)


class DuckDuckGoProvider(SearchProvider):

    def search(
        self,
        query: str,
        max_results: int = 5
    ):

        results = []

        with DDGS() as ddgs:

            response = ddgs.text(
                query,
                max_results=max_results,
            )

            for item in response:

                results.append(

                    SearchResult(

                        title=item.get(
                            "title",
                            ""
                        ),

                        url=item.get(
                            "href",
                            ""
                        ),

                        snippet=item.get(
                            "body",
                            ""
                        ),

                        source="DuckDuckGo",

                    )

                )

        return results