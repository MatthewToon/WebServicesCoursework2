"""Tests for print and find functionality."""

from src.indexer import add_page_to_index
from src.search import format_search_results, print_word, search_index


def build_sample_index() -> dict:
    # Build a small in-memory index so search behaviour is predictable in tests.
    index = {}
    add_page_to_index(index, "https://quotes.toscrape.com/", "Life is good and good friends matter")
    add_page_to_index(index, "https://quotes.toscrape.com/page/2/", "Good friends share good stories")
    add_page_to_index(index, "https://quotes.toscrape.com/page/3/", "Life stories can inspire")
    return index


def test_print_word_returns_readable_output() -> None:
    index = build_sample_index()

    output = print_word(index, "GOOD")

    assert "Word: good" in output
    assert "Found in 2 page(s)." in output
    assert "Frequency: 2" in output


def test_print_word_handles_missing_word() -> None:
    index = build_sample_index()

    output = print_word(index, "missing")

    assert output == 'Word "missing" was not found in the index.'


def test_print_word_handles_empty_input() -> None:
    index = build_sample_index()

    output = print_word(index, "")

    assert output == "Please enter a word to print."


def test_print_word_rejects_multiple_words() -> None:
    index = build_sample_index()

    output = print_word(index, "good friends")

    assert output == "Please enter exactly one word."


def test_search_index_returns_single_word_results_sorted_by_frequency() -> None:
    index = build_sample_index()

    query_words, results = search_index(index, "good")

    assert query_words == ["good"]
    assert [result["url"] for result in results] == [
        "https://quotes.toscrape.com/",
        "https://quotes.toscrape.com/page/2/",
    ]
    assert [result["score"] for result in results] == [2, 2]


def test_search_index_requires_all_words_in_query() -> None:
    index = build_sample_index()

    # Multi-word search is conjunctive: every word must be present.
    query_words, results = search_index(index, "good friends")

    assert query_words == ["good", "friends"]
    assert [result["url"] for result in results] == [
        "https://quotes.toscrape.com/",
        "https://quotes.toscrape.com/page/2/",
    ]
    assert [result["score"] for result in results] == [3, 3]


def test_search_index_returns_empty_when_a_word_is_missing() -> None:
    index = build_sample_index()

    query_words, results = search_index(index, "good impossible")

    assert query_words == ["good", "impossible"]
    assert results == []


def test_search_index_handles_empty_query() -> None:
    index = build_sample_index()

    query_words, results = search_index(index, "")

    assert query_words == []
    assert results == []


def test_format_search_results_handles_empty_query() -> None:
    output = format_search_results([], [])

    assert output == "Please enter a search term."


def test_format_search_results_handles_no_matches() -> None:
    output = format_search_results(["good", "missing"], [])

    assert output == 'No pages found for query: "good missing"'


def test_format_search_results_formats_matches() -> None:
    output = format_search_results(
        ["good", "friends"],
        [
            {"url": "https://quotes.toscrape.com/", "score": 3},
            {"url": "https://quotes.toscrape.com/page/2/", "score": 3},
        ],
    )

    assert "Query: good friends" in output
    assert "Found 2 matching page(s)." in output
    assert "https://quotes.toscrape.com/ (score: 3)" in output
