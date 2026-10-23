"""
Generates multiple-choice quizzes from code diffs.

This module contains the QuizGenerator class, which takes a dictionary of
staged code changes and generates a list of multiple-choice questions. The
questions are designed to test the user's understanding of the specific
changes made to the codebase.
"""

import logging

logger = logging.getLogger(__name__)


class QuizGenerator:
    """
    A class to generate quizzes based on code changes.

    This class processes the output from the GitReader to identify patterns
    in the code diffs and creates corresponding multiple-choice questions.
    """

    def generate_quiz(self, staged_changes: dict[str, str]) -> list[dict]:
        """
        Generate a list of quiz questions from the staged changes.

        Args:
            staged_changes (Dict[str, str]): A dictionary where keys are file
                paths and values are the corresponding diff strings.

        Returns:
            List[Dict]: A list of dictionaries, each representing a quiz
            question with a prompt, correct answer, and incorrect options.
        """
        quiz_questions: list[dict] = []

        for file_path, diff in staged_changes.items():
            added_lines = [
                line[1:]
                for line in diff.splitlines()
                if line.startswith("+") and not line.startswith("+++")
            ]
            removed_lines = [
                line[1:]
                for line in diff.splitlines()
                if line.startswith("-") and not line.startswith("---")
            ]

            # Question 1: How many lines were added?
            added_count = len(added_lines)
            quiz_questions.append(
                {
                    "prompt": f"How many lines were added in {file_path}?",
                    "correct_answer": str(added_count),
                    "incorrect_options": [
                        str(added_count + 1),
                        str(max(added_count - 1, 0)),
                        str(added_count + 2),
                    ],
                }
            )

            # Question 2: How many lines were removed?
            removed_count = len(removed_lines)
            quiz_questions.append(
                {
                    "prompt": f"How many lines were removed in {file_path}?",
                    "correct_answer": str(removed_count),
                    "incorrect_options": [
                        str(removed_count + 1),
                        str(max(removed_count - 1, 0)),
                        str(removed_count + 2),
                    ],
                }
            )

            # Question 3: Which of the following was added?
            if added_lines:
                sample_added = added_lines[0].strip()
                # Create a simple true/false style question
                quiz_questions.append(
                    {
                        "prompt": f"Which of the following lines was added to {file_path}?",
                        "correct_answer": sample_added,
                        "incorrect_options": [
                            removed_lines[0].strip() if removed_lines else "No removal line",
                            "Unrelated line of code",
                            "Another unrelated line",
                        ],
                    }
                )
            else:
                # Fallback generic question if no additions
                quiz_questions.append(
                    {
                        "prompt": f"What type of change was made to {file_path}?",
                        "correct_answer": "Modification",
                        "incorrect_options": ["Deletion", "Creation", "Renaming"],
                    }
                )

        return quiz_questions
