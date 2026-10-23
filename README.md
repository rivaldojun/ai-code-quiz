# ai-code-quiz

A local tool to quiz developers on AI-generated code changes before merging.

![CI](https://github.com/rivaldojun/ai-code-quiz/actions/workflows/ci.yml/badge.svg)

## Why

Developers need a way to confirm they understand AI-generated code changes before merging. This step helps avoid errors and keeps code quality high. Reviewing AI output can be tricky without a reliable check. ai-code-quiz quizzes you on your staged Git diff to ensure you grasp the changes.

## Features

- Reads staged Git diffs and detects Python and JavaScript changes.
- Generates at least three multiple-choice questions per code change.
- Presents quiz questions in a local web interface.
- Allows you to submit answers via the web interface.
- Works entirely offline without calling external servers.

## Installation

Install from GitHub via pip:

```console
$ pip install git+https://github.com/rivaldojun/ai-code-quiz
```

Install from source:

```console
$ git clone https://github.com/rivaldojun/ai-code-quiz.git && cd ai-code-quiz
$ pip install -e "."
```

## Usage

Run the tool in your Git repo to quiz yourself on staged changes:

```console
$ ai-code-quiz --help
usage: ai-code-quiz [-h] [--repo REPO] [--port PORT]

Generate a multiple‑choice quiz from staged Git changes and serve it via a
local web interface.

options:
 -h, --help show this help message and exit
 --repo REPO Path to the Git repository (default: current working
 directory).
 --port PORT Port for the local web server (default: 5000).
```

Example:

```console
$ python -m ai_code_quiz --port 5000
No staged changes detected. Exiting.
```

## How it works

- **src/ai_code_quiz/git_reader.py** reads your staged Git diff and identifies if changes are in Python or JavaScript.
- **src/ai_code_quiz/quiz_generator.py** creates multiple-choice questions based on simple pattern matching of code changes.
- **src/ai_code_quiz/web_server.py** runs a local web server showing the quiz and accepts your answers.
- **src/ai_code_quiz/main.py** coordinates reading diffs, generating quizzes, and serving the interface.
- **src/ai_code_quiz/config.py** holds configuration like default ports and repo paths.

## Limitations

- Quiz questions come from pattern matching and may miss complex logical errors.
- Only Python and JavaScript changes receive quizzes; other languages are ignored.
- The web interface is minimal with no tracking or user accounts.
- The project name is generic and may affect discoverability.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

MIT License
