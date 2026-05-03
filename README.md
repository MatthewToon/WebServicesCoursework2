# Web Services Coursework 2

This repository contains a Python search tool for `https://quotes.toscrape.com/` for the COMP3011 Web Services and Web Data coursework. It crawls the site, builds an inverted index with per-page word statistics, saves and loads the index from disk, and supports simple command-line search commands.

## Project structure

```text
src/
  crawler.py
  indexer.py
  search.py
  main.py
tests/
  test_crawler.py
  test_indexer.py
  test_search.py
  test_main.py
data/
  index.json
requirements.txt
README.md
```

## Requirements

- Python 3.11 or newer
- Internet access when running the `build` command

Install the dependencies with:

```bash
pip install -r requirements.txt
```

## Running

Start the shell from the repository root:

```bash
python -m src.main
```

The shell supports these commands:

- `build`
- `load`
- `print <word>`
- `find <query terms>`
- `help`
- `exit`

Example session:

```text
> build
> load
> print life
> print nonsense
> find good friends
> exit
```

## Index structure

The project uses a dictionary-based inverted index:

```json
{
  "life": {
    "https://quotes.toscrape.com/": {
      "frequency": 2,
      "positions": [5, 42]
    }
  }
}
```

Each word points to a posting list. Each posting stores:

- `frequency`: how many times the word appears on that page
- `positions`: the token positions where the word appears on that page

## Design decisions

- Breadth-first crawling: the web crawling lecture describes crawling as graph traversal, so this project uses a simple breadth-first crawl with a queue and visited set.
- Politeness window: the crawler waits at least 6 seconds between successive requests, matching the coursework brief.
- Simple tokenisation: all text is lowercased and tokenised with the regex `[a-zA-Z0-9]+`, which keeps the behaviour predictable and easy to explain.
- No stemming or stopword removal: the brief does not require them, and keeping the original words makes `print` and `find` behaviour easier to understand.
- Conjunctive search: multi-word `find` queries only return pages containing every query word, using set intersection.
- Simple ranking: results are ranked by the sum of query-term frequencies in each page.

## Testing

Run the automated tests with:

```bash
pytest --cov=src
```

The test suite includes:

- unit tests for tokenisation, indexing, search formatting, and command handling
- crawler tests with mocked HTTP requests and mocked sleeping
- a simple integration-style crawl across fake linked pages
- a lightweight performance-style indexing test

## Manual smoke test

For a small live verification against the real target site, run:

```bash
python scripts/smoke_test_live.py
```

This is separate from the automated test suite. It fetches the real homepage at `https://quotes.toscrape.com/`, checks that the page is reachable, extracts visible text using the crawler logic, and counts internal links using the same link-extraction function as the main crawler.

## Known limitations

- The crawler only indexes visible page text and does not apply advanced weighting to headings, titles, or anchor text.
- Search is case-insensitive but does not support phrase searching, stemming, stopword removal, or TF-IDF ranking.
- The `build` command can take several minutes because the required politeness delay is intentionally enforced.

## GenAI declaration

This project was developed with AI assistance for planning, structure, and edge-case review. The implementation was kept deliberately simple so that every function and design choice can be explained clearly in the coursework video, and advanced suggestions such as PageRank, TF-IDF, async crawling, and stemming were intentionally not used.
