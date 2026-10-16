
import unittest

from campusflow.quiz import collect_answer, collect_explanation, run_quiz
from campusflow.quiz_questions import QUESTIONS


class TestEngineeringQuiz(unittest.TestCase):

    def test_question_bank_contains_six_questions(self):
        self.assertEqual(len(QUESTIONS), 6)

    def test_every_question_has_four_answer_options(self):
        for question in QUESTIONS:
            self.assertEqual(
                set(question["options"].keys()),
                {"A", "B", "C", "D"},
            )
            self.assertIn(question["answer"], question["options"])

    def test_invalid_answer_is_retried(self):
        question = QUESTIONS[0]
        answers = iter(["X", "", "b"])
        messages = []

        answer = collect_answer(
            question,
            input_fn=lambda _: next(answers),
            output_fn=messages.append,
        )

        self.assertEqual(answer, "B")
        self.assertTrue(
            any("Invalid choice" in message for message in messages)
        )

    def test_quiz_returns_score_and_two_explanations(self):
        answers = iter([
            "B",  # Question 1
            "C",  # Question 2
            "The empty dataset has no resolved tickets.",
            "B",  # Question 3
            "C",  # Question 4
            "C",  # Question 5
            "Duplicate IDs make ticket references ambiguous.",
            "B",  # Question 6
        ])

        result = run_quiz(
            input_fn=lambda _: next(answers),
            output_fn=lambda *_: None,
        )

        self.assertEqual(result["score"], 6)
        self.assertEqual(result["total"], 6)
        self.assertEqual(len(result["explanations"]), 2)

    def test_quiz_scores_incorrect_answers(self):
        answers = iter([
            "A",  # Question 1
            "A",  # Question 2
            "The report has no resolved tickets.",
            "A",  # Question 3
            "A",  # Question 4
            "A",  # Question 5
            "Duplicate IDs must be handled safely.",
            "A",  # Question 6
        ])

        result = run_quiz(
            input_fn=lambda _: next(answers),
            output_fn=lambda *_: None,
        )

        self.assertEqual(result["score"], 0)
        self.assertEqual(result["total"], 6)
        self.assertEqual(len(result["explanations"]), 2)

    def test_blank_explanation_is_rejected(self):
        answers = iter(["", "My explanation"])

        explanation = collect_explanation(
            1,
            input_fn=lambda _: next(answers),
            output_fn=lambda *_: None,
        )

        self.assertEqual(explanation, "My explanation")


if __name__ == "__main__":
    unittest.main()
