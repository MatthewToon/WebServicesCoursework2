"""CLI tests."""

from __future__ import annotations

from src.main import HELP_TEXT, handle_command, run_shell


def test_handle_command_returns_help_and_exit() -> None:
    help_message, help_exit = handle_command("help")
    exit_message, should_exit = handle_command("exit")

    assert help_message == HELP_TEXT
    assert help_exit is False
    assert exit_message == "Exiting search tool."
    assert should_exit is True


def test_handle_command_rejects_unknown_commands() -> None:
    message, should_exit = handle_command("dance")

    assert message == "Unknown command"
    assert should_exit is False


def test_handle_command_handles_empty_input() -> None:
    message, should_exit = handle_command("")

    assert message == "Please enter a command."
    assert should_exit is False


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
