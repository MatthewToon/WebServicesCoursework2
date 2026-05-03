"""Main shell entry point for the COMP3011 search tool."""

from __future__ import annotations

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


def handle_command(command: str) -> tuple[str, bool]:
    """Handle shell commands that do not depend on the index yet."""
    cleaned_command = command.strip()

    if not cleaned_command:
        return "Please enter a command.", False

    action = cleaned_command.split(maxsplit=1)[0].lower()

    if action == "help":
        return HELP_TEXT, False

    if action == "exit":
        return "Exiting search tool.", True

    return "Unknown command", False


def run_shell() -> None:
    """Run the interactive shell."""
    print(HELP_TEXT)

    while True:
        try:
            command = input("> ")
        except EOFError:
            print("\nExiting search tool.")
            break

        message, should_exit = handle_command(command)
        print(message)

        if should_exit:
            break


if __name__ == "__main__":
    run_shell()
