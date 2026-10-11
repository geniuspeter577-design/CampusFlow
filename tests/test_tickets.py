import unittest

from campusflow.tickets import (
    calculate_priority,
    create_ticket,
    generate_ticket_id,
    validate_affected_users,
    validate_category,
    validate_title,
    validate_urgency,
)


class TestTicketValidation(unittest.TestCase):
    def test_valid_title_is_trimmed(self):
        self.assertEqual(validate_title("  Wi-Fi is down  "), "Wi-Fi is down")

    def test_blank_title_rejected(self):
        for title in ("", "   ", None):
            with self.subTest(title=title), self.assertRaises(ValueError):
                validate_title(title)

    def test_category_normalization(self):
        self.assertEqual(validate_category("NETWORK"), "Network")
        self.assertEqual(validate_category(" hardware "), "Hardware")

    def test_invalid_category_rejected(self):
        with self.assertRaises(ValueError):
            validate_category("Electricity")

    def test_non_text_category_rejected(self):
        with self.assertRaises(ValueError):
            validate_category(None)

    def test_urgency_normalization(self):
        self.assertEqual(validate_urgency(" HIGH "), "high")

    def test_invalid_urgency_rejected(self):
        with self.assertRaises(ValueError):
            validate_urgency("urgent")

    def test_non_text_urgency_rejected(self):
        with self.assertRaises(ValueError):
            validate_urgency(None)

    def test_valid_affected_users(self):
        self.assertEqual(validate_affected_users(5), 5)

    def test_invalid_affected_users_rejected(self):
        for value in (0, -1, 1.5, True, "3", None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_affected_users(value)

    def test_critical_priority(self):
        self.assertEqual(calculate_priority("high", 12), "critical")

    def test_high_priority(self):
        self.assertEqual(calculate_priority("high", 4), "high")
        self.assertEqual(calculate_priority("low", 10), "high")

    def test_medium_priority(self):
        self.assertEqual(calculate_priority("medium", 1), "medium")
        self.assertEqual(calculate_priority("low", 3), "medium")

    def test_low_priority(self):
        self.assertEqual(calculate_priority("low", 1), "low")

    def test_priority_rejects_invalid_inputs(self):
        with self.assertRaises(ValueError):
            calculate_priority("urgent", 1)
        with self.assertRaises(ValueError):
            calculate_priority("low", True)

    def test_first_ticket_id(self):
        self.assertEqual(generate_ticket_id([]), "T001")

    def test_next_ticket_id(self):
        tickets = [{"id": "T001"}, {"id": "T002"}]
        self.assertEqual(generate_ticket_id(tickets), "T003")

    def test_ticket_id_after_gap(self):
        tickets = [{"id": "T001"}, {"id": "T003"}, {"id": "T007"}]
        self.assertEqual(generate_ticket_id(tickets), "T008")

    def test_ticket_creation(self):
        ticket = create_ticket([], "Network down", "network", "high", 12)
        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["title"], "Network down")
        self.assertEqual(ticket["category"], "Network")
        self.assertEqual(ticket["urgency"], "high")
        self.assertEqual(ticket["affected_users"], 12)
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])

    def test_ticket_ids_increment(self):
        first = create_ticket([], "First", "Software", "low", 1)
        second = create_ticket([first], "Second", "Hardware", "low", 1)
        self.assertEqual(second["id"], "T002")

    def test_ticket_creation_rejects_blank_title(self):
        with self.assertRaises(ValueError):
            create_ticket([], "  ", "Other", "low", 1)

    def test_ticket_creation_rejects_invalid_category(self):
        with self.assertRaises(ValueError):
            create_ticket([], "Problem", "Food", "low", 1)

    def test_ticket_creation_rejects_invalid_urgency(self):
        with self.assertRaises(ValueError):
            create_ticket([], "Problem", "Other", "urgent", 1)

    def test_ticket_creation_rejects_invalid_affected_users(self):
        with self.assertRaises(ValueError):
            create_ticket([], "Problem", "Other", "low", True)


if __name__ == "__main__":
    unittest.main()
