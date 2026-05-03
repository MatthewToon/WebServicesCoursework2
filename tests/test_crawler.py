"""Tests for crawler behaviour and link extraction."""

from __future__ import annotations

from src.crawler import extract_internal_links, extract_page_text


def test_extract_page_text_removes_script_content() -> None:
    html = """
    <html>
      <body>
        <h1>Quotes</h1>
        <script>ignore me</script>
        <p>Life is good.</p>
      </body>
    </html>
    """

    text = extract_page_text(html)

    assert "Quotes" in text
    assert "Life is good." in text
    assert "ignore me" not in text


def test_extract_internal_links_normalizes_filters_and_deduplicates() -> None:
    html = """
    <html>
      <body>
        <a href="/page/2/">Next</a>
        <a href="https://quotes.toscrape.com/page/2/#top">Duplicate with fragment</a>
        <a href="https://example.com/">External</a>
        <a href="mailto:test@example.com">Mail</a>
      </body>
    </html>
    """

    links = extract_internal_links(html, "https://quotes.toscrape.com/")

    assert links == ["https://quotes.toscrape.com/page/2/"]
