# Web Services Coursework 2

## 1. Project Overview & Purpose

This project is a Python command-line search tool for `https://quotes.toscrape.com/`, created for the COMP3011 Web Services and Web Data coursework.

The tool:

- crawls pages from `quotes.toscrape.com`
- respects the required 6-second politeness window between requests
- extracts visible page text using BeautifulSoup
- builds an inverted index of word occurrences
- stores word statistics including frequency and token positions
- saves the completed index to `data/index.json`
- reloads the saved index from disk
- supports `build`, `load`, `print <word>`, and `find <query terms>` commands

The implementation is intentionally simple and explainable. It uses breadth-first crawling, regex tokenisation, dictionary-based index storage, and conjunctive search for multi-word queries. Advanced ranking features such as TF-IDF and PageRank are not included because the coursework plan focused on the required crawler, indexer, storage, and basic retrieval behaviour.

Project structure:

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
scripts/
  smoke_test_live.py
data/
  index.json
requirements.txt
README.md
```

## 2. Installation/Setup Instructions

Clone the repository and move into the project folder:

```powershell
git clone https://github.com/MatthewToon/WebServicesCoursework2.git
cd WebServicesCoursework2
```

Install the dependencies using Python 3.11:

```powershell
py -3.11 -m pip install -r requirements.txt
```

Start the program from the repository root:

```powershell
py -3.11 -m src.main
```

If using a virtual environment instead:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m src.main
```

Internet access is required for `build`, because that command crawls the live target website.

## 3. Usage Examples (for all four commands)

The program runs as an interactive shell. After starting it with `py -3.11 -m src.main`, enter commands at the `>` prompt.

### `build`

```text
> build
```

`build` crawls `https://quotes.toscrape.com/`, extracts page text, builds the inverted index, and saves it to `data/index.json`.

The command can take several minutes because the crawler waits 6 seconds between successive requests. When it finishes, it reports the number of crawled pages, the number of unique indexed words, and the saved index path.

### `load`

```text
> load
```

`load` reads the saved index from `data/index.json` back into memory. This lets the user search without crawling the website again.

This command only works after `build` has already created the index file.

### `print <word>`

```text
> print born
```

`print <word>` displays the inverted-index entry for one word. It shows each page containing that word, the word frequency on that page, and the token positions where the word appears.

Example edge case:

```text
> print nonsenseword
```

This returns a clear message if the word is not found in the index.

### `find <query terms>`

```text
> find good friends
```

`find <query terms>` searches for pages containing all query terms. Multi-word queries use conjunctive search, so a page must contain every query word to be returned.

Examples:

```text
> find born died
> find world thinking miracle
> find
```

`find born died` is useful for checking that author pages were crawled. `find` with no search terms demonstrates the empty-query edge case.

## 4. Testing Instructions

Run the automated test suite with:

```powershell
py -3.11 -m pytest -q
```

The test suite covers:

- tokenisation and inverted-index construction
- frequency and position tracking
- JSON save/load behaviour
- `print` and `find` search behaviour
- multi-word conjunctive queries
- missing-word and empty-query edge cases
- command-line shell handling
- crawler parsing and internal-link extraction
- mocked successful and failed HTTP requests
- mocked politeness delay behaviour

To run the tests and show coverage, use:

```powershell
@'
from coverage import Coverage
import pytest

cov = Coverage(source=["src"], data_file=None)
cov.start()

exit_code = pytest.main(["-q"])

cov.stop()
cov.report(show_missing=True)

raise SystemExit(exit_code)
'@ | py -3.11 -
```

This runs the normal pytest suite and reports statement coverage for the `src` folder. The project has been verified at 99% statement coverage.

There is also a small live smoke test:

```powershell
py -3.11 scripts/smoke_test_live.py
```

The smoke test fetches the real homepage, checks the HTTP status, extracts visible text, and counts internal links using the same parsing helpers as the crawler. It is not a full crawl and should finish quickly.

## 5. Any dependencies and how to install them

The project dependencies are listed in `requirements.txt`:

```text
beautifulsoup4
pytest
pytest-cov
requests
```

Install all dependencies with:

```powershell
py -3.11 -m pip install -r requirements.txt
```

Dependency purpose:

- `requests` is used to make HTTP requests during crawling.
- `beautifulsoup4` is used to parse HTML and extract text and links.
- `pytest` is used for the automated test suite.
- `pytest-cov` provides standard pytest coverage support.

Python 3.11 is recommended because the project was developed and tested with `py -3.11`.
