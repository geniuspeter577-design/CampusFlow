
"""Tests for safe JSON ticket storage."""

import json
import tempfile
import unittest
from pathlib import Path

from campusflow.storage import load_tickets, save_tickets


def make_ticket(ticket_id="T001"):
    return {
        "id": ticket_id,
        "title": "Network is down",
        "category": "Network",
        "urgency": "high",
        "affected_users": 12,
        "priority": "critical",
        "status": "open",
        "assigned_to": None,
        "notes": [],
    }


class TestStorage(unittest.TestCase):

    def test_missing_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "missing.json"
            self.assertEqual(load_tickets(path), [])

    def test_save_and_load_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            tickets = [make_ticket()]

            save_tickets(tickets, path)

            self.assertEqual(load_tickets(path), tickets)

    def test_malformed_json_raises_clear_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            path.write_text("{broken", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "malformed"):
                load_tickets(path)

    def test_non_list_json_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            path.write_text(
                json.dumps({"id": "T001"}),
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_duplicate_ticket_ids_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            path.write_text(
                json.dumps([
                    make_ticket("T001"),
                    make_ticket("T001"),
                ]),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "Duplicate ticket ID"):
                load_tickets(path)

    def test_invalid_note_structure_is_rejected(self):
        ticket = make_ticket()
        ticket["notes"] = [{"note_id": "N001", "author": "Reuben"}]

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            path.write_text(json.dumps([ticket]), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "invalid structure"):
                load_tickets(path)

    def test_invalid_collection_does_not_mutate_original_tickets(self):
        first_ticket = make_ticket("T001")
        second_ticket = make_ticket("T002")
        first_ticket.pop("notes")
        second_ticket.pop("notes")
        second_ticket["status"] = "invalid_status"
        tickets = [first_ticket, second_ticket]
        original_tickets = json.loads(json.dumps(tickets))

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"

            with self.assertRaises(ValueError):
                save_tickets(tickets, path)

            self.assertFalse(path.exists())

        self.assertEqual(tickets, original_tickets)

    def test_ticket_id_continues_after_reload(self):
        from campusflow.tickets import create_ticket

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            tickets = [make_ticket("T001"), make_ticket("T003")]

            save_tickets(tickets, path)
            loaded_tickets = load_tickets(path)

            new_ticket = create_ticket(
                loaded_tickets,
                "Printer is offline",
                "Hardware",
                "medium",
                2,
            )

            self.assertEqual(new_ticket["id"], "T004")

    def test_note_id_continues_after_reload(self):
        from campusflow.workflow import add_note

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            ticket = make_ticket()
            ticket["notes"] = [
                {
                    "note_id": "N001",
                    "author": "Reuben",
                    "message": "Initial troubleshooting completed.",
                },
                {
                    "note_id": "N003",
                    "author": "Gongbede",
                    "message": "Waiting for network confirmation.",
                },
            ]

            save_tickets([ticket], path)
            loaded_tickets = load_tickets(path)

            new_note = add_note(
                "T001",
                "Reuben",
                "Testing note ID continuity.",
                loaded_tickets,
            )

            self.assertEqual(new_note["note_id"], "N004")

    def test_failed_save_preserves_existing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            original_tickets = [make_ticket()]
            save_tickets(original_tickets, path)
            original_contents = path.read_text(encoding="utf-8")

            invalid_tickets = [make_ticket()]
            invalid_tickets[0]["status"] = "invalid_status"

            with self.assertRaises(ValueError):
                save_tickets(invalid_tickets, path)

            self.assertEqual(
                path.read_text(encoding="utf-8"),
                original_contents,
            )
            self.assertEqual(load_tickets(path), original_tickets)


    def test_ticket_notes_survive_save_and_load(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            tickets = [
                {
                    "id": "T001",
                    "status": "open",
                    "notes": [
                        "Contacted the network team",
                        "Waiting for a response",
                    ],
                }
            ]

            save_tickets(tickets, path)
            loaded_tickets = load_tickets(path)

            self.assertEqual(loaded_tickets, tickets)
            self.assertEqual(
                loaded_tickets[0]["notes"],
                [
                    "Contacted the network team",
                    "Waiting for a response",
                ],
            )

if __name__ == "__main__":
    unittest.main()
