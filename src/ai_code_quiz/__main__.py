"""
Entry point for ``python -m ai_code_quiz``.

Running the package as a module invokes the same CLI entry point used by the
installed console script.  This mirrors the behaviour of many standard‑library
tools (e.g., ``python -m http.server``) and satisfies the test suite that
executes the package with ``-m``.
"""

from __future__ import annotations

import sys

from .cli import main


def _run() -> int:
    """Execute the CLI and return its exit status."""
    return main()


if __name__ == "__main__":
    sys.exit(_run())
