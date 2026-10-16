
import unittest

from campusflow.workflow import (
    add_note,
    assign_ticket,
    update_ticket_status,
    get_open_ticket_queue,
)


class TestWorkflow(unittest.TestCase):

    def setUp(self):
        self.ticket = {
            "id": "T001",
            "title": "Network is down",
            "category": "Network",
            "urgency": "high",
            "affected_users": 12,
            "priority": "critical",
            "status": "open",
            "assigned_to": None,
            "notes": [],
        }

    def test_assign_ticket(self):
        assign_ticket(self.ticket, "Reuben")
        self.assertEqual(self.ticket["assigned_to"], "Reuben")

    def test_assignee_spaces_are_removed(self):
        assign_ticket(self.ticket, "  Reuben  ")
        self.assertEqual(self.ticket["assigned_to"], "Reuben")

    def test_empty_assignee_is_rejected(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.ticket, "   ")

    def test_resolved_ticket_cannot_be_reassigned(self):
        self.ticket["status"] = "resolved"
        with self.assertRaises(ValueError):
            assign_ticket(self.ticket, "Reuben")

    def test_reopened_ticket_can_be_reassigned(self):
        self.ticket["status"] = "resolved"
        update_ticket_status(self.ticket, "open")
        assign_ticket(self.ticket, "Reuben")
        self.assertEqual(self.ticket["assigned_to"], "Reuben")

    def test_non_text_assignee_is_rejected(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.ticket, None)

    def test_update_status_to_in_progress(self):
        self.ticket["assigned_to"] = "Reuben"
        update_ticket_status(self.ticket, "in_progress")
        self.assertEqual(self.ticket["status"], "in_progress")

    def test_unassigned_ticket_cannot_start(self):
        with self.assertRaises(ValueError):
            update_ticket_status(self.ticket, "in_progress")

    def test_invalid_status_is_rejected(self):
        with self.assertRaises(ValueError):
            update_ticket_status(self.ticket, "pending")

    def test_status_is_normalized(self):
        self.ticket["assigned_to"] = "Reuben"
        update_ticket_status(self.ticket, " IN_PROGRESS ")
        self.assertEqual(self.ticket["status"], "in_progress")

    def test_resolved_ticket_must_be_reopened(self):
        self.ticket["status"] = "resolved"
        with self.assertRaises(ValueError):
            update_ticket_status(self.ticket, "in_progress")

    def test_resolved_ticket_can_be_reopened(self):
        self.ticket["status"] = "resolved"
        update_ticket_status(self.ticket, "open")
        self.assertEqual(self.ticket["status"], "open")

    def test_queue_sorts_by_priority(self):
        tickets = [
            {"id": "T001", "priority": "low", "status": "open"},
            {"id": "T002", "priority": "critical", "status": "open"},
            {"id": "T003", "priority": "high", "status": "open"},
        ]
        queue = get_open_ticket_queue(tickets)
        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T002", "T003", "T001"],
        )

    def test_queue_sorts_equal_priorities_by_numeric_id(self):
        tickets = [
            {"id": "T010", "priority": "high", "status": "open"},
            {"id": "T002", "priority": "high", "status": "open"},
            {"id": "T005", "priority": "high", "status": "open"},
        ]
        queue = get_open_ticket_queue(tickets)
        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T002", "T005", "T010"],
        )

    def test_queue_excludes_non_open_tickets(self):
        tickets = [
            {"id": "T001", "priority": "critical", "status": "resolved"},
            {"id": "T002", "priority": "high", "status": "in_progress"},
            {"id": "T003", "priority": "low", "status": "open"},
        ]
        queue = get_open_ticket_queue(tickets)
        self.assertEqual([ticket["id"] for ticket in queue], ["T003"])

    def test_empty_queue(self):
        self.assertEqual(get_open_ticket_queue([]), [])

    def test_add_valid_note(self):
        note = add_note(
            "T001",
            " Reuben ",
            "Restarted the network router.",
            [self.ticket],
        )
        self.assertEqual(note["note_id"], "N001")
        self.assertEqual(note["author"], "Reuben")
        self.assertEqual(note["message"], "Restarted the network router.")
        self.assertEqual(len(self.ticket["notes"]), 1)

    def test_invalid_note_does_not_consume_id(self):
        tickets = [self.ticket]

        with self.assertRaises(ValueError):
            add_note("T001", "Reuben", "bad", tickets)

        note = add_note(
            "T001",
            "Reuben",
            "Checked the network connection.",
            tickets,
        )
        self.assertEqual(note["note_id"], "N001")

    def test_resolved_ticket_rejects_note(self):
        self.ticket["status"] = "resolved"

        with self.assertRaises(ValueError):
            add_note(
                "T001",
                "Reuben",
                "Checked the network connection.",
                [self.ticket],
            )

    def test_reopened_ticket_accepts_note(self):
        self.ticket["status"] = "resolved"
        update_ticket_status(self.ticket, "open")

        note = add_note(
            "T001",
            "Reuben",
            "Checked the network connection.",
            [self.ticket],
        )
        self.assertEqual(note["note_id"], "N001")

    def test_note_rejects_missing_ticket(self):
        with self.assertRaises(ValueError):
            add_note(
                "T999",
                "Reuben",
                "Checked the network connection.",
                [self.ticket],
            )

    def test_malformed_existing_note_is_rejected(self):
        self.ticket["notes"] = [None]

        with self.assertRaisesRegex(ValueError, "valid note objects"):
            add_note(
                self.ticket["id"],
                "Reuben",
                "Checking malformed note data.",
                [self.ticket],
            )

    def test_note_author_is_trimmed(self):
        note = add_note(
            "T001",
            "  Reuben  ",
            "Checked the network connection.",
            [self.ticket],
        )
        self.assertEqual(note["author"], "Reuben")

    def test_note_message_is_trimmed(self):
        note = add_note(
            "T001",
            "Reuben",
            "  Checked the network connection.  ",
            [self.ticket],
        )
        self.assertEqual(
            note["message"],
            "Checked the network connection.",
        )

    def test_note_message_over_300_characters_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "5 to 300"):
            add_note(
                "T001",
                "Reuben",
                "x" * 301,
                [self.ticket],
            )
        self.assertEqual(self.ticket["notes"], [])


if __name__ == "__main__":
    unittest.main()
