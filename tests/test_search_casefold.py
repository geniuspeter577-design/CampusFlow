import unittest

from campusflow.search import search_tickets


def make(ticket_id, title):
    return {
        "id": ticket_id, "title": title, "category": "Network",
        "status": "open", "priority": "high", "assigned_to": None,
    }


class TestSearchCasefold(unittest.TestCase):

    def test_casefold_matches_german_double_s(self):
        tickets = [make("T001", "Straße lamp broken")]
        self.assertEqual(len(search_tickets(tickets, title="STRASSE")), 1)

    def test_same_punctuation_needed_for_match(self):
        tickets = [make("T001", "Wi-Fi down")]
        self.assertEqual(search_tickets(tickets, title="wifi"), [])
        self.assertEqual(len(search_tickets(tickets, title="WI-FI")), 1)


if __name__ == "__main__":
    unittest.main()
