"""CLI tests."""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from src.indexer import save_index
from src.main import HELP_TEXT, handle_command, run_shell


def test_handle_command_returns_help_and_exit() -> None:
    index = {}

    _, help_message, help_exit = handle_command("help", index)
    _, exit_message, should_exit = handle_command("exit", index)

    assert help_message == HELP_TEXT
    assert help_exit is False
    assert exit_message == "Exiting search tool."
    assert should_exit is True


def test_handle_command_rejects_unknown_commands() -> None:
    _, message, should_exit = handle_command("dance", {})

    assert message == "Unknown command"
    assert should_exit is False


def test_handle_command_handles_empty_input() -> None:
    _, message, should_exit = handle_command("", {})

    assert message == "Please enter a command."
    assert should_exit is False


def test_handle_command_load_reads_saved_index() -> None:
    index_path = Path("data") / f"test-load-{uuid4().hex}.json"
    fake_index = {
        "good": {
            "https://quotes.toscrape.com/": {
                "frequency": 2,
                "positions": [0, 1],
            }
        }
    }
    try:
        save_index(fake_index, index_path)

        updated_index, message, should_exit = handle_command("load", None, index_path)

        assert updated_index == fake_index
        assert "Loaded index from" in message
        assert should_exit is False
    finally:
        if index_path.exists():
            try:
                index_path.unlink()
            except PermissionError:
                pass


def test_handle_command_requires_index_for_print_and_find() -> None:
    _, print_message, _ = handle_command("print life", None)
    _, find_message, _ = handle_command("find life", None)

    assert print_message == "No index loaded. Run build or load first."
    assert find_message == "No index loaded. Run build or load first."


def test_handle_command_load_missing_file_reports_error() -> None:
    _, message, should_exit = handle_command("load", None, Path("data") / "missing-index.json")

    assert message == "No saved index found. Run build first."
    assert should_exit is False


def test_handle_command_print_and_find_with_loaded_index() -> None:
    index = {
        "life": {
            "https://quotes.toscrape.com/": {
                "frequency": 1,
                "positions": [0],
            }
        },
        "good": {
            "https://quotes.toscrape.com/": {
                "frequency": 2,
                "positions": [1, 2],
            }
        },
    }

    _, print_message, _ = handle_command("print life", index)
    _, find_message, _ = handle_command("find good", index)

    assert "Word: life" in print_message
    assert "Query: good" in find_message


def test_run_shell_prints_help_and_exits(monkeypatch) -> None:
    commands = iter(["help", "exit"])
    printed_lines = []

    monkeypatch.setattr("builtins.input", lambda prompt: next(commands))
    monkeypatch.setattr(
        "builtins.print",
        lambda *args, **kwargs: printed_lines.append(" ".join(str(arg) for arg in args)),
    )

    run_shell()

    assert printed_lines[0] == HELP_TEXT
    assert HELP_TEXT in printed_lines[1]
    assert printed_lines[-1] == "Exiting search tool."
