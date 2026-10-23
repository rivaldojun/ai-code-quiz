"""
Command‑line entry point for *ai‑code‑quiz*.

The ``main`` function parses command‑line arguments, reads staged Git changes,
generates a quiz, and launches the local Flask web server.  All operations are
performed locally; no external network access is required.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .config import DEFAULT_PORT
from .git_reader import GitReader
from .quiz_generator import QuizGenerator
from .web_server import start_server


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """
    Build and parse the command‑line arguments.

    Args:
        argv: Optional list of arguments (defaults to ``sys.argv[1:]``).

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        prog="ai-code-quiz",
        description=(
            "Generate a multiple‑choice quiz from staged Git changes and "
            "serve it via a local web interface."
        ),
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path.cwd(),
        help="Path to the Git repository (default: current working directory).",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Port for the local web server (default: {DEFAULT_PORT}).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """
    Entry point used by the console script.

    The function returns an exit code (0 for success, non‑zero for failure) so
    that it can be used both as a CLI command and from unit tests.

    Args:
        argv: Optional list of command‑line arguments; if ``None`` the
              arguments are taken from ``sys.argv``.

    Returns:
        Exit status code.
    """
    args = _parse_args(argv)

    try:
        # ------------------------------------------------------------------
        # 1. Read staged changes from the repository.
        # ------------------------------------------------------------------
        git_reader = GitReader(args.repo)
        staged_changes: dict[str, str] = git_reader.get_staged_changes()

        if not staged_changes:
            print("No staged changes detected. Exiting.")
            return 0

        # ------------------------------------------------------------------
        # 2. Generate quiz questions from the diffs.
        # ------------------------------------------------------------------
        generator = QuizGenerator()
        quiz = generator.generate_quiz(staged_changes)

        # ------------------------------------------------------------------
        # 3. Launch the Flask web server (blocking call).
        # ------------------------------------------------------------------
        # ``run=True`` starts the development server; this blocks until the
        # user stops it (Ctrl‑C).  All work is performed offline.
        start_server(args.port, quiz, run=True)

        return 0
    except Exception as exc:  # pragma: no cover – defensive programming
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
