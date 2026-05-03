"""Breadth-first crawler helpers for quotes.toscrape.com."""

from __future__ import annotations

import time
from urllib.parse import urldefrag, urljoin, urlparse

import requests
from bs4 import BeautifulSoup

if __package__:
    from .indexer import Index, add_page_to_index
else:  # pragma: no cover - supports direct execution
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).resolve().parent))
    from indexer import Index, add_page_to_index

BASE_URL = "https://quotes.toscrape.com/"
DEFAULT_HEADERS = {
    "User-Agent": "COMP3011 Search Tool",
}


def extract_page_text(html: str) -> str:
    """Extract the visible text from an HTML page."""
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    container = soup.body or soup
    return container.get_text(" ", strip=True)


def extract_internal_links(
    html: str,
    current_url: str,
    base_url: str = BASE_URL,
) -> list[str]:
    """Find unique internal links and convert them to absolute URLs."""
    soup = BeautifulSoup(html, "html.parser")
    allowed_domain = urlparse(base_url).netloc
    links: list[str] = []
    seen_links: set[str] = set()

    for anchor in soup.find_all("a", href=True):
        full_url = urljoin(current_url, anchor["href"])
        full_url = urldefrag(full_url)[0]
        parsed_url = urlparse(full_url)

        if parsed_url.scheme not in {"http", "https"}:
            continue

        if parsed_url.netloc != allowed_domain:
            continue

        if full_url in seen_links:
            continue

        seen_links.add(full_url)
        links.append(full_url)

    return links


def crawl_site(
    start_url: str = BASE_URL,
    politeness_delay: int = 6,
    headers: dict[str, str] | None = None,
) -> Index:
    """Crawl the target site and build an inverted index."""
    index: Index = {}
    queue = [start_url]
    queued_urls = {start_url}
    visited_urls: set[str] = set()
    request_count = 0
    active_headers = headers or DEFAULT_HEADERS

    while queue:
        current_url = queue.pop(0)
        queued_urls.discard(current_url)

        if current_url in visited_urls:
            continue

        visited_urls.add(current_url)
        print(f"Crawling: {current_url}")

        if request_count > 0:
            time.sleep(politeness_delay)

        request_count = request_count + 1

        try:
            response = requests.get(current_url, headers=active_headers, timeout=10)
        except requests.RequestException:
            print(f"Failed to fetch: {current_url}")
            continue

        if response.status_code != 200:
            print(f"Skipping URL with status code {response.status_code}: {current_url}")
            continue

        html = response.text
        text = extract_page_text(html)
        add_page_to_index(index, current_url, text)

        for link in extract_internal_links(html, current_url, start_url):
            if link in visited_urls or link in queued_urls:
                continue

            queue.append(link)
            queued_urls.add(link)

    return index
