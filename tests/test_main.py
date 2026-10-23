"""
Tests for the ``main`` entry point, focusing on offline operation.

The test ensures that invoking ``main`` does not attempt any network
communication and that it exits cleanly when no staged changes are present.
"""

from src.ai_code_quiz.main import main


def test_ac4_offline_operation(tmp_path, monkeypatch):
    """
    Run ``main`` in an environment without internet access and with an empty
    repository.  The function should complete without raising and return 0.
    """
    # Create an empty git repository (no staged changes).
    repo_path = tmp_path / "empty_repo"
    repo_path.mkdir()
    # Initialise git – this does not require network access.
    import subprocess

    subprocess.run(["git", "init"], cwd=repo_path, check=True)

    # Ensure that any attempt to open a network socket raises an error.
    # The simplest way is to monkey‑patch ``socket.create_connection``.
    import socket

    def forbidden(*args, **kwargs):
        raise RuntimeError("Network access is forbidden during tests")

    monkeypatch.setattr(socket, "create_connection", forbidden)

    # Run the CLI entry point pointing at the empty repository.
    exit_code = main(["--repo", str(repo_path), "--port", "0"])
    assert exit_code == 0
