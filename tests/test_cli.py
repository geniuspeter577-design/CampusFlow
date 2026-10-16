import unittest

from campusflow.cli import ask_valid, format_ticket_row


def fake_input(answers):
    answers = iter(answers)
    return lambda prompt: next(answers)


class TestCli(unittest.TestCase):

    def test_valid_answer_is_accepted(self):
        result = ask_valid("? ", ("a", "b"), fake_input(["a"]), lambda m: None)
        self.assertEqual(result, "a")

    def test_invalid_answer_reprompts_then_accepts(self):
        messages = []
        result = ask_valid("? ", ("a", "b"), fake_input(["z", "9", "B"]), messages.append)
        self.assertEqual(result, "b")
        self.assertEqual(len(messages), 2)

    def test_empty_answer_allowed_when_listed(self):
        result = ask_valid("? ", ("", "open"), fake_input(["  "]), lambda m: None)
        self.assertEqual(result, "")

    def test_row_shows_unassigned(self):
        ticket = {"id": "T001", "title": "Wi-Fi", "category": "Network",
                  "priority": "high", "status": "open", "assigned_to": None}
        self.assertIn("unassigned", format_ticket_row(ticket))


if __name__ == "__main__":
    unittest.main()
