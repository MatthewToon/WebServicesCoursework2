"""Small live smoke test against quotes.toscrape.com.

This is a manual verification helper, not part of the automated pytest suite.
It fetches the real homepage, extracts visible text, and counts internal links.
"""

from pathlib import Path
import sys

import requests

# Add the repository root so the script can import the src package.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.crawler import BASE_URL, DEFAULT_HEADERS, extract_internal_links, extract_page_text


def main() -> None:
    """Run a minimal live check against the real target website."""
    # This script uses the same request headers and parsing helpers as the main app.
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
