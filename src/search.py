"""Search and display helpers for the inverted index."""

from __future__ import annotations

if __package__:
    from .indexer import Index, tokenize
else:  # pragma: no cover - supports direct execution
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).resolve().parent))
    from indexer import Index, tokenize

SearchResult = dict[str, object]


def print_word(index: Index, word: str) -> str:
    """Return a readable view of the postings for one word."""
    words = tokenize(word)

    if not words:
        return "Please enter a word to print."

    if len(words) != 1:
        return "Please enter exactly one word."

    normalized_word = words[0]
    postings = index.get(normalized_word)

    if postings is None:
        return f'Word "{normalized_word}" was not found in the index.'

    lines = [
        f"Word: {normalized_word}",
        f"Found in {len(postings)} page(s).",
        "",
    ]

    for url in sorted(postings):
        posting = postings[url]
        lines.append(url)
        lines.append(f"Frequency: {posting['frequency']}")
        lines.append(f"Positions: {posting['positions']}")
        lines.append("")

    return "\n".join(lines).rstrip()


def search_index(index: Index, query: str) -> tuple[list[str], list[SearchResult]]:
    """Run a conjunctive multi-word search against the index."""
    query_words = tokenize(query)

    if not query_words:
        return [], []

    matching_urls: set[str] | None = None

    for word in query_words:
        if word not in index:
            return query_words, []

        urls_for_word = set(index[word].keys())

        if matching_urls is None:
            matching_urls = urls_for_word
        else:
            matching_urls = matching_urls.intersection(urls_for_word)

    results: list[SearchResult] = []

    for url in matching_urls or set():
        score = 0

        for word in query_words:
            score = score + int(index[word][url]["frequency"])

        results.append(
            {
                "url": url,
                "score": score,
            }
        )

    results.sort(key=lambda result: (-int(result["score"]), str(result["url"])))

    return query_words, results


def format_search_results(query_words: list[str], results: list[SearchResult]) -> str:
    """Return a readable view of search results."""
    if not query_words:
        return "Please enter a search term."

    normalized_query = " ".join(query_words)

    if not results:
        return f'No pages found for query: "{normalized_query}"'

    lines = [
        f"Query: {normalized_query}",
        f"Found {len(results)} matching page(s).",
        "",
    ]

    for result in results:
        lines.append(f"{result['url']} (score: {result['score']})")

    return "\n".join(lines)
