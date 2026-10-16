import tempfile
import unittest
from pathlib import Path

from campusflow.explanations import (
    ask_explanation, run_check_with_explanations, save_explanations,
)
from campusflow.question_bank import QUESTIONS


def fake_input(answers):
    answers = iter(answers)
    return lambda prompt: next(answers)


class TestExplanations(unittest.TestCase):

    def test_short_explanation_reprompts(self):
        messages = []
        text = ask_explanation("? ", fake_input(["no", "   ", "It keeps data safe"]),
                               messages.append)
        self.assertEqual(text, "It keeps data safe")
        self.assertEqual(len(messages), 2)

    def test_explanations_are_saved_to_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "notes" / "check.md"
            save_explanations([("Q1", "B", "Reject keeps data unchanged")],
                              path, today="2026-10-16")
            content = path.read_text(encoding="utf-8")
            self.assertIn("Q1", content)
            self.assertIn("Reject keeps data unchanged", content)

    def test_full_flow_saves_two_and_score_ignores_text(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "check.md"
            typed = ([q["answer"].lower() for q in QUESTIONS]
                     + ["too short", "A long enough but unrelated reply",
                        "Another long enough explanation"])
            score, entries = run_check_with_explanations(
                QUESTIONS, fake_input(typed), lambda m: None, path)
            self.assertEqual(score, 6)
            self.assertEqual(len(entries), 2)
            self.assertEqual(path.read_text(encoding="utf-8").count("- **Q"), 2)


if __name__ == "__main__":
    unittest.main()
