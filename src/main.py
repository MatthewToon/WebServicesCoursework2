"""Main shell entry point for the COMP3011 search tool."""

from __future__ import annotations

from pathlib import Path

if __package__:
    from .indexer import Index, load_index
    from .search import format_search_results, print_word, search_index
else:  # pragma: no cover - supports direct execution
    import sys

    sys.path.append(str(Path(__file__).resolve().parent))
    from indexer import Index, load_index
    from search import format_search_results, print_word, search_index

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

DEFAULT_INDEX_PATH = Path(__file__).resolve().parent.parent / "data" / "index.json"


def load_existing_index(index_path: str | Path = DEFAULT_INDEX_PATH) -> tuple[Index, str]:
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
    index: Index | None,
    index_path: str | Path = DEFAULT_INDEX_PATH,
) -> tuple[Index | None, str, bool]:
    """Handle shell commands."""
    cleaned_command = command.strip()

    if not cleaned_command:
        return index, "Please enter a command.", False

    parts = cleaned_command.split(maxsplit=1)
    action = parts[0].lower()
    argument = parts[1] if len(parts) > 1 else ""

    if action == "build":
        if argument:
            return index, "Usage: build", False

        return index, "Build is not implemented yet.", False

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
    index: Index | None = None
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
