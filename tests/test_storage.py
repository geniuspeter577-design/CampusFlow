import json
import tempfile
import unittest
from pathlib import Path

from campusflow.storage import load_tickets, save_tickets


class TestStorage(unittest.TestCase):
    def test_missing_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(load_tickets(Path(directory) / "missing.json"), [])

    def test_save_and_load_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            tickets = [{"id": "T001", "status": "open"}]
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
            path.write_text(json.dumps({"id": "T001"}), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_tickets(path)


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
