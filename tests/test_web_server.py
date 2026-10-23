"""
Tests for the web server functionality, including rendering and submission.
"""

import pytest
from flask import Flask

from src.ai_code_quiz.web_server import start_server


@pytest.fixture
def sample_quiz():
    """Provide a sample quiz for testing the web interface."""
    return [
        {
            "prompt": "What is the capital of France?",
            "correct_answer": "Paris",
            "incorrect_options": ["London", "Berlin", "Madrid"],
        }
    ]


def test_ac3_web_interface(sample_quiz):
    """Verify that the web interface displays questions and allows submission."""
    app = Flask(__name__)
    start_server(5000, sample_quiz)

    # Simulate a GET request to the root
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200
        assert "Paris" in response.data.decode()  # Check if correct answer is displayed

        # Simulate a POST request to submit
        response = client.post("/submit", data={"answer": "Paris"})
        assert response.status_code == 200
        assert "Answers submitted!" in response.data.decode()
