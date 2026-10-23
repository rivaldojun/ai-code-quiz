"""
Utilities for reading staged changes from a Git repository.

The :class:`GitReader` class abstracts the interaction with *GitPython* and
provides a simple ``dict`` mapping file paths to their diff strings.
"""

from __future__ import annotations

from pathlib import Path

import git
from git import Repo, exc


class GitReader:
    """
    Reads staged changes from a Git repository.

    Parameters
    ----------
    repo_path :
        Path to the root of a Git repository.

    Raises
    ------
    ValueError
        If ``repo_path`` does not exist or is not a valid Git repository.
    """

    def __init__(self, repo_path: Path) -> None:
        if not repo_path.is_dir():
            raise ValueError("Invalid Git repository: path does not exist")
        try:
            self.repo: Repo = git.Repo(repo_path)
        except git.exc.InvalidGitRepositoryError as exc:
            raise ValueError("Invalid Git repository") from exc

    def get_staged_changes(self) -> dict[str, str]:
        """
        Return a mapping of file paths to diff strings for staged changes.

        The method first attempts to obtain the diff between the index and
        ``HEAD`` (i.e., staged changes).  If the repository has no commits yet,
        ``HEAD`` does not exist and a ``BadName`` error is raised; in that case
        we fall back to using ``git diff --cached`` which works for an empty
        repository.  If there are still no staged changes, we finally compare the
        index with the working tree to surface any unstaged modifications.

        Returns
        -------
        dict[str, str]
            Keys are file paths (relative to the repository root) and values
            are the textual diff for that file.
        """
        staged_changes: dict[str, str] = {}

        # 1️⃣ Try the normal staged‑vs‑HEAD diff.
        try:
            diff_index = self.repo.index.diff("HEAD")
            for item in diff_index:
                file_path = item.a_path or item.b_path
                diff_text = item.diff.decode("utf-8")
                staged_changes[file_path] = diff_text
        except exc.BadName:
            # Repository is empty (no HEAD). Use ``git diff --cached`` which
            # reports staged additions/removals against an empty tree.
            # First, obtain the list of staged files.
            staged_files = self.repo.git.diff("--cached", "--name-only").splitlines()
            for file_path in staged_files:
                diff_text = self.repo.git.diff("--cached", file_path)
                staged_changes[file_path] = diff_text

        # 2️⃣ If nothing was staged, fall back to a full index‑vs‑working‑tree diff.
        if not staged_changes:
            diff_index = self.repo.index.diff(None)
            for item in diff_index:
                file_path = item.a_path or item.b_path
                diff_text = item.diff.decode("utf-8")
                staged_changes[file_path] = diff_text

        return staged_changes
