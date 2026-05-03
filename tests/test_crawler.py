"""Tests for crawler behaviour and link extraction."""

from __future__ import annotations

from unittest.mock import patch

import requests

from src.crawler import crawl_site, extract_internal_links, extract_page_text


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


class FakeResponse:
    """Simple fake response object for crawler tests."""

    def __init__(self, text: str, status_code: int = 200) -> None:
        self.text = text
        self.status_code = status_code


@patch("src.crawler.time.sleep")
@patch("src.crawler.requests.get")
def test_crawl_site_builds_index_across_multiple_pages(mock_get, mock_sleep) -> None:
    page_one = """
    <html>
      <body>
        <p>Life is good.</p>
        <a href="/page/2/">Next</a>
        <a href="/page/2/#top">Next again</a>
      </body>
    </html>
    """
    page_two = """
    <html>
      <body>
        <p>Good friends share stories.</p>
      </body>
    </html>
    """

    def fake_get(url, headers=None, timeout=10):  # noqa: ANN001
        if url == "https://quotes.toscrape.com/":
            return FakeResponse(page_one)

        if url == "https://quotes.toscrape.com/page/2/":
            return FakeResponse(page_two)

        raise AssertionError(f"Unexpected URL requested: {url}")

    mock_get.side_effect = fake_get

    index = crawl_site(politeness_delay=6)

    assert index["life"]["https://quotes.toscrape.com/"]["frequency"] == 1
    assert index["good"]["https://quotes.toscrape.com/"]["frequency"] == 1
    assert index["good"]["https://quotes.toscrape.com/page/2/"]["frequency"] == 1
    assert index["friends"]["https://quotes.toscrape.com/page/2/"]["positions"] == [1]
    assert mock_get.call_count == 2
    mock_sleep.assert_called_once_with(6)


@patch("src.crawler.requests.get")
def test_crawl_site_handles_failed_requests(mock_get) -> None:
    mock_get.side_effect = requests.RequestException("boom")

    index = crawl_site()

    assert index == {}


@patch("src.crawler.requests.get")
def test_crawl_site_skips_non_200_responses(mock_get) -> None:
    mock_get.return_value = FakeResponse("<html></html>", status_code=404)

    index = crawl_site()

    assert index == {}
