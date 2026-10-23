"""
Command‑line interface wrapper.

The ``ai_code_quiz`` console script points to ``ai_code_quiz.cli:main``.
This thin wrapper simply forwards to :func:`ai_code_quiz.main.main`.
"""

from __future__ import annotations

import sys

from .main import main as _main


def main(argv: list[str] | None = None) -> int:
    """
    CLI entry point used by ``setup.cfg`` / ``pyproject.toml``.

    Returns the exit status from :func:`ai_code_quiz.main.main`.
    """
    return _main(argv)


if __name__ == "__main__":
    sys.exit(main())
