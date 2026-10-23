# Contributing to ai-code-quiz

Thanks for taking the time to help. Bug reports, fixes and small focused features are welcome.

## Before you start

- For anything bigger than a small fix, open an issue first so we can agree on the approach.
- Keep pull requests focused on one change. The scope of the project is described in the README;
  features listed there under "Limitations" or out of scope may be declined.

## Development setup

```console
git clone https://github.com/rivaldojun/ai-code-quiz.git
cd ai-code-quiz
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
ruff check .
ruff format --check .
pytest -q
```

These are the same checks the CI runs on every pull request.

## Pull requests

- Add or update tests for the behaviour you change. Tests must not need network access.
- Run the checks above and make sure they pass.
- Describe what changed and why in the pull request.

## Reporting bugs

Open an issue with the version you use, the exact command or code, what you expected and what happened.
Never paste API keys or private data in an issue.

## License

By contributing, you agree that your contributions are licensed under the MIT license of this project.
