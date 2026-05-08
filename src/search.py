"""Search and display helpers for the inverted index."""

from .indexer import tokenize


def print_word(index: dict, word: str) -> str:
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


def build_result_sort_key(result: dict) -> tuple[int, str]:
    """Sort higher scores first, then sort URLs alphabetically."""
    score = int(result["score"])
    url = str(result["url"])
    return (-score, url)


def search_index(index: dict, query: str) -> tuple[list[str], list[dict]]:
    """Run a conjunctive multi-word search against the index."""
    query_words = tokenize(query)

    if not query_words:
        return [], []

    matching_urls: set[str] | None = None

    # This is a conjunctive search:
    # a page must contain every query word to be returned.
    for word in query_words:
        if word not in index:
            return query_words, []

        urls_for_word = set(index[word].keys())

        if matching_urls is None:
            matching_urls = urls_for_word
        else:
            matching_urls = matching_urls.intersection(urls_for_word)

    if matching_urls is None:
        return query_words, []

    results: list[dict] = []

    for url in matching_urls:
        score = 0

        for word in query_words:
            score = score + index[word][url]["frequency"]

        results.append(
            {
                "url": url,
                "score": score,
            }
        )

    results.sort(key=build_result_sort_key)

    return query_words, results


def format_search_results(query_words: list[str], results: list[dict]) -> str:
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
