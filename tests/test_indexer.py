"""Tests for text tokenisation and inverted index construction."""

from __future__ import annotations

import time
from pathlib import Path
from uuid import uuid4

from src.indexer import add_page_to_index, load_index, save_index, tokenize


def test_tokenize_lowercases_and_splits_punctuation() -> None:
    assert tokenize("Good, GOOD! Friends-and-family.") == [
        "good",
        "good",
        "friends",
        "and",
        "family",
    ]


def test_add_page_to_index_tracks_frequency_and_positions() -> None:
    index = {}

    add_page_to_index(index, "https://quotes.toscrape.com/", "Good good life!")

    assert index["good"]["https://quotes.toscrape.com/"]["frequency"] == 2
    assert index["good"]["https://quotes.toscrape.com/"]["positions"] == [0, 1]
    assert index["life"]["https://quotes.toscrape.com/"]["frequency"] == 1
    assert index["life"]["https://quotes.toscrape.com/"]["positions"] == [2]


def test_add_page_to_index_handles_empty_text() -> None:
    index = {}

    add_page_to_index(index, "https://quotes.toscrape.com/", "")

    assert index == {}


def test_numbers_are_indexed() -> None:
    index = {}

    add_page_to_index(index, "https://quotes.toscrape.com/", "Room 101 and 2025")

    assert index["101"]["https://quotes.toscrape.com/"]["positions"] == [1]
    assert index["2025"]["https://quotes.toscrape.com/"]["positions"] == [3]


def test_save_and_load_index_round_trip() -> None:
    index = {}
    file_path = Path("data") / f"test-index-{uuid4().hex}.json"

    try:
        add_page_to_index(index, "https://quotes.toscrape.com/", "Life is good")
        save_index(index, file_path)

        loaded_index = load_index(file_path)

        assert loaded_index == index
    finally:
        if file_path.exists():
            try:
                file_path.unlink()
            except PermissionError:
                pass


def test_add_page_to_index_handles_large_repeated_input_quickly() -> None:
    text = "word " * 20000
    index = {}
    started_at = time.perf_counter()

    add_page_to_index(index, "https://quotes.toscrape.com/", text)

    elapsed = time.perf_counter() - started_at

    assert elapsed < 2
    assert index["word"]["https://quotes.toscrape.com/"]["frequency"] == 20000
