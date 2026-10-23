"""
Tests for the QuizGenerator class, focusing on question generation.
"""

import pytest

from src.ai_code_quiz.quiz_generator import QuizGenerator


@pytest.fixture
def sample_diff():
    """Provide a sample diff string for testing."""
    return {
        "example.py": """
diff --git a/example.py b/example.py
index 1234567..8901234 100644
--- a/example.py
+++ b/example.py
@@ -1,5 +1,5 @@
 def greet(name):
-    return "Hello, " + name + "!"
+    return f"Hello, {name}!"
"""
    }


def test_ac2_generates_questions(sample_diff):
    """Verify that the QuizGenerator produces at least 3 valid questions."""
    generator = QuizGenerator()
    quiz = generator.generate_quiz(sample_diff)

    assert len(quiz) >= 3
    for question in quiz:
        assert "prompt" in question
        assert "correct_answer" in question
        assert "incorrect_options" in question
        assert len(question["incorrect_options"]) > 0
