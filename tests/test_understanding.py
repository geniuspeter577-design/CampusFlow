import unittest

from campusflow.question_bank import QUESTIONS
from campusflow.understanding_check import run_check, score_answers


def fake_input(answers):
    answers = iter(answers)
    return lambda prompt: next(answers)


class TestUnderstandingCheck(unittest.TestCase):

    def test_bank_has_six_valid_questions(self):
        self.assertEqual(len(QUESTIONS), 6)
        for q in QUESTIONS:
            self.assertEqual(set(q["options"]), {"A", "B", "C", "D"})
            self.assertIn(q["answer"], q["options"])

    def test_all_correct_scores_six(self):
        correct = [q["answer"] for q in QUESTIONS]
        self.assertEqual(score_answers(QUESTIONS, correct), 6)

    def test_all_wrong_scores_zero(self):
        wrong = ["A" if q["answer"] != "A" else "B" for q in QUESTIONS]
        self.assertEqual(score_answers(QUESTIONS, wrong), 0)

    def test_mixed_answers_score_actual_choices(self):
        answers = [q["answer"] for q in QUESTIONS]
        answers[0] = "A" if answers[0] != "A" else "B"
        self.assertEqual(score_answers(QUESTIONS, answers), 5)

    def test_invalid_answer_reprompts_then_scores(self):
        messages = []
        typed = ["z"] + [q["answer"].lower() for q in QUESTIONS]
        score, _ = run_check(QUESTIONS, fake_input(typed), messages.append)
        self.assertEqual(score, 6)
        self.assertTrue(any("Invalid choice" in m for m in messages))


if __name__ == "__main__":
    unittest.main()
