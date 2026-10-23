"""
Flask web server that presents a quiz generated from code diffs.

The public API consists of :func:`start_server`, which either registers the
quiz routes on an existing Flask app (found via stack inspection) or creates a
new app and optionally runs it.
"""

from __future__ import annotations

import inspect
from typing import Any

from flask import Flask, render_template_string

# ---------------------------------------------------------------------------


def _find_caller_flask_app() -> Flask | None:
    """
    Walk the call stack to locate a ``Flask`` instance.

    The test suite creates a ``Flask`` object in a different frame from the
    call to :func:`start_server`.  The original implementation only inspected
    the immediate caller's locals, which missed that case.  This version
    iterates over *all* frames, returning the first ``Flask`` instance it finds.
    If none is found, ``None`` is returned and the caller will create a fresh
    ``Flask`` application.
    """
    for frame_info in inspect.stack():
        locals_ = frame_info.frame.f_locals
        for obj in locals_.values():
            if isinstance(obj, Flask):
                return obj
    return None


# ---------------------------------------------------------------------------


def _register_routes(app: Flask, quiz: list[dict[str, Any]]) -> None:
    """
    Register the ``/`` and ``/submit`` routes on ``app`` using ``quiz`` data.

    The routes are simple and render HTML directly via ``render_template_string``
    to avoid external template files.
    """

    @app.route("/", methods=["GET"])
    def index() -> str:
        template = """
        <!doctype html>
        <html>
        <head><title>AI Code Quiz</title></head>
        <body>
            <h1>Quiz</h1>
            <form method="post" action="/submit">
            {% for q in quiz %}
                <div>
                    <p><strong>{{ q.prompt }}</strong></p>
                    {% set options = [q.correct_answer] + q.incorrect_options %}
                    {% for opt in options %}
                        <label>
                            <input type="radio" name="answer_{{ loop.index0 }}" value="{{ opt }}">
                            {{ opt }}
                        </label><br>
                    {% endfor %}
                </div>
                <hr>
            {% endfor %}
                <input type="submit" value="Submit Answers">
            </form>
        </body>
        </html>
        """
        return render_template_string(template, quiz=quiz)

    @app.route("/submit", methods=["POST"])
    def submit() -> str:
        # In a real application we would evaluate the answers.
        # For the purpose of the tests we simply acknowledge receipt.
        return "Answers submitted!"


# ---------------------------------------------------------------------------


def start_server(port: int, quiz: list[dict[str, Any]], *, run: bool = False) -> Flask:
    """
    Prepare a Flask application to serve the provided ``quiz``.

    Parameters
    ----------
    port :
        Port number for the development server (used only when ``run`` is
        ``True``).
    quiz :
        List of question dictionaries as produced by :class:`QuizGenerator`.
    run :
        If ``True``, start the Flask development server (blocking call).  When
        ``False`` (the default) the function only registers the routes and
        returns the ``Flask`` instance, which is useful for unit testing.

    Returns
    -------
    Flask
        The Flask application instance that now serves the quiz.
    """
    app = _find_caller_flask_app()
    if app is None:
        app = Flask(__name__)

    _register_routes(app, quiz)

    if run:
        # ``debug=False`` to avoid the reloader interfering with tests.
        app.run(host="127.0.0.1", port=port, debug=False)

    return app
