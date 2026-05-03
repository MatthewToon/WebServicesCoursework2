"""Breadth-first crawler helpers for quotes.toscrape.com."""

from __future__ import annotations

from urllib.parse import urldefrag, urljoin, urlparse

from bs4 import BeautifulSoup

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
