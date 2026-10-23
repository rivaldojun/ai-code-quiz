"""
Tests for the GitReader class, focusing on reading staged changes.
"""

from pathlib import Path

import pytest

from src.ai_code_quiz.git_reader import GitReader


@pytest.fixture
def sample_repo(tmp_path):
    """Create a temporary Git repository with a staged change."""
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir()
    (repo_path / "example.py").write_text("print('Hello, world!')")
    (repo_path / "example.js").write_text("console.log('Hello, world!');")

    # Initialize git and stage a change
    import subprocess

    subprocess.run(["git", "init"], cwd=repo_path)
    subprocess.run(["git", "add", "example.py"], cwd=repo_path)

    return repo_path


def test_ac1_parses_valid_file(sample_repo):
    """Verify that the GitReader correctly identifies a staged Python file."""
    reader = GitReader(sample_repo)
    staged_changes = reader.get_staged_changes()

    assert "example.py" in staged_changes
    assert "example.js" not in staged_changes  # Only .py was staged
    assert "diff" in staged_changes["example.py"]  # Check for diff content


def test_invalid_repo_path():
    """Check that an error is raised when the repository path is invalid."""
    with pytest.raises(ValueError, match="Invalid Git repository"):
        GitReader(Path("/non/existent/path"))
