"""Main shell entry point for the COMP3011 search tool."""

from pathlib import Path

from .crawler import BASE_URL, crawl_site
from .indexer import load_index, save_index
from .search import format_search_results, print_word, search_index

# Keep the help text visible in one place so the shell and tests match.
HELP_TEXT = "\n".join(
    [
        "Search Tool",
        "Commands:",
        "  build",
        "  load",
        "  print <word>",
        "  find <query terms>",
        "  help",
        "  exit",
    ]
)

# The saved index lives in the data folder at the repository root.
DEFAULT_INDEX_PATH = Path(__file__).resolve().parent.parent / "data" / "index.json"


def count_indexed_pages(index: dict) -> int:
    """Count how many unique page URLs appear anywhere in the index."""
    page_urls: set[str] = set()

    for word_entries in index.values():
        for url in word_entries:
            page_urls.add(url)

    return len(page_urls)


def build_index(index_path: str | Path = DEFAULT_INDEX_PATH) -> tuple[dict, str]:
    """Build the index by crawling the target site."""
    index = crawl_site(start_url=BASE_URL)
    page_count = count_indexed_pages(index)

    # Save immediately so a later `load` command can reuse the crawl.
    save_index(index, index_path)

    message = "\n".join(
        [
            "Build complete.",
            f"Crawled {page_count} page(s).",
            f"Indexed {len(index)} unique words.",
            f"Saved index to {Path(index_path)}",
        ]
    )

    return index, message


def load_existing_index(index_path: str | Path = DEFAULT_INDEX_PATH) -> tuple[dict, str]:
    """Load the saved index from disk."""
    index = load_index(index_path)
    message = "\n".join(
        [
            f"Loaded index from {Path(index_path)}",
            f"Index contains {len(index)} unique words.",
        ]
    )
    return index, message


def handle_command(
    command: str,
    index: dict | None,
    index_path: str | Path = DEFAULT_INDEX_PATH,
) -> tuple[dict | None, str, bool]:
    """Handle shell commands."""
    cleaned_command = command.strip()

    if not cleaned_command:
        return index, "Please enter a command.", False

    # Split once so the rest of the line stays intact for multi-word queries.
    parts = cleaned_command.split(maxsplit=1)
    action = parts[0].lower()
    argument = parts[1] if len(parts) > 1 else ""

    if action == "build":
        if argument:
            return index, "Usage: build", False

        new_index, message = build_index(index_path)
        return new_index, message, False

    if action == "load":
        if argument:
            return index, "Usage: load", False

        try:
            new_index, message = load_existing_index(index_path)
        except FileNotFoundError:
            return index, "No saved index found. Run build first.", False

        return new_index, message, False

    if action == "print":
        if index is None:
            return index, "No index loaded. Run build or load first.", False

        return index, print_word(index, argument), False

    if action == "find":
        if index is None:
            return index, "No index loaded. Run build or load first.", False

        query_words, results = search_index(index, argument)
        return index, format_search_results(query_words, results), False

    if action == "help":
        return index, HELP_TEXT, False

    if action == "exit":
        return index, "Exiting search tool.", True

    return index, "Unknown command", False


def run_shell(index_path: str | Path = DEFAULT_INDEX_PATH) -> None:
    """Run the interactive shell."""
    # The shell keeps the currently loaded index in memory between commands.
    index = None
    print(HELP_TEXT)

    while True:
        try:
            command = input("> ")
        except EOFError:
            print("\nExiting search tool.")
            break

        index, message, should_exit = handle_command(command, index, index_path)
        print(message)

        if should_exit:
            break


if __name__ == "__main__":
    run_shell()
