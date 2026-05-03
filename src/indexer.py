"""Utilities for tokenising text and building an inverted index."""

from __future__ import annotations

import json
import re
from pathlib import Path

Index = dict[str, dict[str, dict[str, object]]]

TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9]+")


def tokenize(text: str) -> list[str]:
    """Convert text into lowercase alphanumeric tokens."""
    if not text:
        return []

    return TOKEN_PATTERN.findall(text.lower())


def add_page_to_index(index: Index, url: str, text: str) -> Index:
    """Add all tokens from one page into the inverted index."""
    words = tokenize(text)

    for position, word in enumerate(words):
        if word not in index:
            index[word] = {}

        if url not in index[word]:
            index[word][url] = {
                "frequency": 0,
                "positions": [],
            }

        posting = index[word][url]
        posting["frequency"] = int(posting["frequency"]) + 1
        positions = posting["positions"]

        if isinstance(positions, list):
            positions.append(position)

    return index


def save_index(index: Index, file_path: str | Path) -> None:
    """Save the full index into one JSON file."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(index, file, indent=2)


def load_index(file_path: str | Path) -> Index:
    """Load an index from disk."""
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return data
