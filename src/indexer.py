"""Utilities for tokenising text and building an inverted index."""

import json
import re
from pathlib import Path

# Keep tokenisation simple and close to the coursework brief:
# lowercase words made from letters and numbers.
TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9]+")


def tokenize(text: str) -> list[str]:
    """Convert text into lowercase alphanumeric tokens."""
    if not text:
        return []

    return TOKEN_PATTERN.findall(text.lower())


def add_page_to_index(index: dict, url: str, text: str) -> dict:
    """Add all tokens from one page into the inverted index."""
    words = tokenize(text)

    # The position is the token number inside this page.
    for position, word in enumerate(words):
        # Each word has a posting list containing the pages where it appears.
        if word not in index:
            index[word] = {}

        # Each page stores the statistics required by the brief.
        if url not in index[word]:
            index[word][url] = {
                "frequency": 0,
                "positions": [],
            }

        index[word][url]["frequency"] = index[word][url]["frequency"] + 1
        index[word][url]["positions"].append(position)

    return index


def save_index(index: dict, file_path: str | Path) -> None:
    """Save the full index into one JSON file."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(index, file, indent=2)


def load_index(file_path: str | Path) -> dict:
    """Load an index from disk."""
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return data
