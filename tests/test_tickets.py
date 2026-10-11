import unittest

from campusflow.tickets import (
    validate_title,
    validate_category,
    validate_urgency,
    validate_affected_users,
    calculate_priority,
    generate_ticket_id,
    create_ticket,
)


class TestTicketValidation(unittest.TestCase):

    # Title validation
    def test_valid_title(self):
        result = validate_title("Wi-Fi is down")
        self.assertEqual(result, "Wi-Fi is down")

    def test_blank_title(self):
        with self.assertRaises(ValueError):
            validate_title("   ")

    # Category validation
    def test_category_normalization(self):
        result = validate_category("NETWORK")
        self.assertEqual(result, "Network")

    def test_invalid_category(self):
        with self.assertRaises(ValueError):
            validate_category("Electricity")

    # Urgency validation
    def test_urgency_normalization(self):
        result = validate_urgency("HIGH")
        self.assertEqual(result, "high")

    def test_invalid_urgency(self):
        with self.assertRaises(ValueError):
            validate_urgency("urgent")

    # Affected users validation
    def test_valid_affected_users(self):
        result = validate_affected_users(5)
        self.assertEqual(result, 5)

    def test_zero_affected_users(self):
        with self.assertRaises(ValueError):
            validate_affected_users(0)

    def test_negative_affected_users(self):
        with self.assertRaises(ValueError):
            validate_affected_users(-2)

    def test_decimal_affected_users(self):
        with self.assertRaises(ValueError):
            validate_affected_users(5.5)

    # Priority calculation
    def test_critical_priority(self):
        self.assertEqual(calculate_priority("high", 12), "critical")

    def test_high_priority(self):
        self.assertEqual(calculate_priority("high", 4), "high")

    def test_medium_priority(self):
        self.assertEqual(calculate_priority("medium", 5), "medium")

    def test_low_priority(self):
        self.assertEqual(calculate_priority("low", 1), "low")

    # Ticket ID generation
    def test_first_ticket_id(self):
        self.assertEqual(generate_ticket_id([]), "T001")

    def test_next_ticket_id(self):
        tickets = [{"id": "T001"}, {"id": "T002"}]
        self.assertEqual(generate_ticket_id(tickets), "T003")

    def test_ticket_id_after_deletion(self):
        tickets = [
            {"id": "T001"},
            {"id": "T003"},
            {"id": "T007"},
        ]

        self.assertEqual(generate_ticket_id(tickets), "T008")

    # Ticket creation
    def test_create_ticket(self):
        ticket = create_ticket(
            "Wi-Fi is down",
            "NETWORK",
            "HIGH",
            12,
            [],
        )

        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["title"], "Wi-Fi is down")
        self.assertEqual(ticket["category"], "Network")
        self.assertEqual(ticket["urgency"], "high")
        self.assertEqual(ticket["affected_users"], 12)
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])

    def test_create_ticket_with_blank_title(self):
        with self.assertRaises(ValueError):
            create_ticket("   ", "NETWORK", "HIGH", 12, [])

    def test_create_ticket_with_invalid_urgency(self):
        with self.assertRaises(ValueError):
            create_ticket("Wi-Fi is down", "NETWORK", "urgent", 12, [])


if __name__ == "__main__":
    unittest.main()