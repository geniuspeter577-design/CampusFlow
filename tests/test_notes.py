import unittest

from campusflow.tickets import add_ticket_note, create_ticket


class TestTicketNotes(unittest.TestCase):
    def setUp(self):
        self.ticket = create_ticket(
            [], "Network is down", "Network", "high", 5
        )

    def test_new_ticket_starts_with_empty_notes(self):
        self.assertEqual(self.ticket["notes"], [])

    def test_add_note(self):
        add_ticket_note(self.ticket, "Contacted the network team")
        self.assertEqual(
            self.ticket["notes"],
            ["Contacted the network team"],
        )

    def test_note_is_trimmed(self):
        add_ticket_note(self.ticket, "  Waiting for a response  ")
        self.assertEqual(
            self.ticket["notes"],
            ["Waiting for a response"],
        )

    def test_multiple_notes_are_preserved_in_order(self):
        add_ticket_note(self.ticket, "First update")
        add_ticket_note(self.ticket, "Second update")
        self.assertEqual(
            self.ticket["notes"],
            ["First update", "Second update"],
        )

    def test_blank_note_is_rejected(self):
        for note in ("", "   "):
            with self.subTest(note=note), self.assertRaises(ValueError):
                add_ticket_note(self.ticket, note)

    def test_non_text_note_is_rejected(self):
        with self.assertRaises(ValueError):
            add_ticket_note(self.ticket, None)


if __name__ == "__main__":
    unittest.main()
