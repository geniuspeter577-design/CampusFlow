import unittest

from campusflow.tickets import create_ticket, calculate_priority


class TestTickets(unittest.TestCase):
    def test_ticket_creation(self):
        ticket = create_ticket([], "Network down", "network", "high", 12)
        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["category"], "Network")
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])

    def test_ids_increment(self):
        first = create_ticket([], "First", "Software", "low", 1)
        second = create_ticket([first], "Second", "Hardware", "low", 1)
        self.assertEqual(second["id"], "T002")

    def test_title_must_not_be_blank(self):
        with self.assertRaises(ValueError):
            create_ticket([], "  ", "Other", "low", 1)

    def test_invalid_category_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket([], "Problem", "Food", "low", 1)

    def test_invalid_urgency_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket([], "Problem", "Other", "urgent", 1)

    def test_affected_users_must_be_positive_integer(self):
        for value in (0, -1, 1.5, True, "3"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    create_ticket([], "Problem", "Other", "low", value)

    def test_priority_rules(self):
        cases = [
            ("high", 10, "critical"),
            ("high", 2, "high"),
            ("low", 10, "high"),
            ("medium", 1, "medium"),
            ("low", 3, "medium"),
            ("low", 2, "low"),
        ]
        for urgency, affected, expected in cases:
            with self.subTest(urgency=urgency, affected=affected):
                self.assertEqual(
                    calculate_priority(urgency, affected), expected
                )


if __name__ == "__main__":
    unittest.main()
