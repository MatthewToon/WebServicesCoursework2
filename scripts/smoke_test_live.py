"""Small live smoke test against quotes.toscrape.com.

This is a manual verification helper, not part of the automated pytest suite.
It fetches the real homepage, extracts visible text, and counts internal links.
"""

from __future__ import annotations

import requests

from src.crawler import BASE_URL, DEFAULT_HEADERS, extract_internal_links, extract_page_text


def main() -> None:
    """Run a minimal live check against the real target website."""
    response = requests.get(BASE_URL, headers=DEFAULT_HEADERS, timeout=10)
    response.raise_for_status()

    page_text = extract_page_text(response.text)
    internal_links = extract_internal_links(response.text, BASE_URL)

    print(f"Status: {response.status_code}")
    print("Text sample:")
    print(page_text[:300])
    print()
    print(f"Internal links found: {len(internal_links)}")
    print("First five links:")

    for link in internal_links[:5]:
        print(link)


if __name__ == "__main__":
    main()
