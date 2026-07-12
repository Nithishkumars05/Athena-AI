from services.search_service import search_service


def main():

    print("=" * 80)
    print("Athena AI Search Test")
    print("=" * 80)

    query = "Latest AI news"

    print(f"\nSearching for: {query}\n")

    results = search_service.search(
        query=query,
        max_results=5
    )

    if not results:
        print("No results found.")
        return

    for i, result in enumerate(results, start=1):

        print(f"[{i}] {result.title}")
        print(result.url)
        print(result.snippet)
        print("-" * 80)


if __name__ == "__main__":
    main()