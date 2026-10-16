import copy
import unittest

from campusflow.notes import add_note, get_notes, next_note_id
from campusflow.workflow import assign_ticket, update_ticket_status


def make_ticket(status="open"):
    return {
        "id": "T001", "title": "Wi-Fi down", "category": "Network",
        "urgency": "high", "affected_users": 12, "priority": "critical",
        "status": status, "assigned_to": None, "notes": [],
    }


class TestNotes(unittest.TestCase):

    def setUp(self):
        self.tickets = [make_ticket()]

    def test_valid_note_gets_first_id(self):
        note = add_note(self.tickets, "T001", "Mentor A", "Router reboot attempted")
        self.assertEqual(note["note_id"], "N001")
        self.assertEqual(note["author"], "Mentor A")

    def test_second_note_gets_second_id(self):
        add_note(self.tickets, "T001", "Mentor A", "Router reboot attempted")
        note = add_note(self.tickets, "T001", "Mentor B", "Checking switch ports")
        self.assertEqual(note["note_id"], "N002")

    def test_bad_notes_rejected_and_ticket_unchanged(self):
        before = copy.deepcopy(self.tickets)
        for author, message in [("", "Long enough note"), ("  ", "Long enough note"),
                                ("Mentor A", "hi"), ("Mentor A", "     "),
                                ("Mentor A", "x" * 301), ("Mentor A", None)]:
            with self.subTest(author=author, message=message):
                with self.assertRaises(ValueError):
                    add_note(self.tickets, "T001", author, message)
        self.assertEqual(self.tickets, before)

    def test_rejected_note_does_not_consume_id(self):
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Mentor A", "hi")
        note = add_note(self.tickets, "T001", "Mentor A", "Proper long note")
        self.assertEqual(note["note_id"], "N001")

    def test_boundary_lengths(self):
        add_note(self.tickets, "T001", "A", "12345")
        add_note(self.tickets, "T001", "A", "x" * 300)
        self.assertEqual(len(get_notes(self.tickets, "T001")), 2)

    def test_resolved_rejects_note_reopen_accepts(self):
        add_note(self.tickets, "T001", "Mentor A", "First note here")
        add_note(self.tickets, "T001", "Mentor B", "Second note here")
        update_ticket_status(self.tickets[0], "resolved")
        before = copy.deepcopy(self.tickets)
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Mentor A", "Third note here")
        self.assertEqual(self.tickets, before)
        update_ticket_status(self.tickets[0], "open")
        note = add_note(self.tickets, "T001", "Mentor A", "Third note here")
        self.assertEqual(note["note_id"], "N003")
        self.assertEqual(len(get_notes(self.tickets, "T001")), 3)

    def test_in_progress_accepts_note(self):
        assign_ticket(self.tickets[0], "Reuben")
        update_ticket_status(self.tickets[0], "in_progress")
        note = add_note(self.tickets, "T001", "Mentor A", "Working on it now")
        self.assertEqual(note["note_id"], "N001")

    def test_unknown_ticket_rejected(self):
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T999", "Mentor A", "Long enough note")

    def test_notes_are_per_ticket(self):
        second = make_ticket()
        second["id"] = "T002"
        self.tickets.append(second)
        add_note(self.tickets, "T001", "A", "Note on ticket one")
        note = add_note(self.tickets, "T002", "A", "Note on ticket two")
        self.assertEqual(note["note_id"], "N001")

    def test_old_plain_text_notes_do_not_break_ids(self):
        self.tickets[0]["notes"] = ["old text note"]
        self.assertEqual(next_note_id(self.tickets[0]), "N001")


if __name__ == "__main__":
    unittest.main()
