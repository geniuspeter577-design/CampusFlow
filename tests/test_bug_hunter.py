import json
import tempfile
import unittest
from pathlib import Path

from campusflow.notes import next_note_id
from campusflow.storage import load_validated_tickets


class TestBugHunter(unittest.TestCase):

    def test_boolean_affected_users_in_file_is_rejected_on_load(self):
        bad = [{"id": "T001", "title": "Bool test", "category": "Network",
                "urgency": "low", "affected_users": True, "priority": "low",
                "status": "open", "assigned_to": None, "notes": []}]
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            path.write_text(json.dumps(bad), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_validated_tickets(path)

    def test_next_note_id_uses_highest_number_not_count(self):
        ticket = {"notes": [
            {"note_id": "N001", "author": "A", "message": "first note"},
            {"note_id": "N003", "author": "B", "message": "third note"},
        ]}
        self.assertEqual(next_note_id(ticket), "N004")


if __name__ == "__main__":
    unittest.main()
