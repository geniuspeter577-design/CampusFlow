import unittest

from campusflow.search import search_tickets


class TestSearchTickets(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            {
                "id": "T001",
                "title": "Network connection failure",
                "category": "Network",
                "status": "open",
                "priority": "high",
            },
            {
                "id": "T002",
                "title": "Laptop screen damaged",
                "category": "Hardware",
                "status": "in_progress",
                "priority": "medium",
            },
            {
                "id": "T003",
                "title": "Network printer unavailable",
                "category": "Network",
                "status": "resolved",
                "priority": "low",
            },
        ]

    def test_title_search_is_case_insensitive(self):
        results = search_tickets(self.tickets, title="NETWORK")
        self.assertEqual([ticket["id"] for ticket in results], ["T001", "T003"])

    def test_combined_filters_use_and_logic(self):
        results = search_tickets(
            self.tickets,
            title="network",
            category="Network",
            status="open",
            priority="high",
        )
        self.assertEqual([ticket["id"] for ticket in results], ["T001"])

    def test_empty_filters_return_all_tickets(self):
        results = search_tickets(self.tickets)
        self.assertEqual(results, self.tickets)

    def test_no_matches_returns_empty_list(self):
        results = search_tickets(self.tickets, title="missing")
        self.assertEqual(results, [])

    def test_search_does_not_modify_original_list(self):
        original = [ticket.copy() for ticket in self.tickets]
        search_tickets(self.tickets, category="Network")
        self.assertEqual(self.tickets, original)

    def test_filter_values_ignore_case_and_surrounding_spaces(self):
        results = search_tickets(
            self.tickets,
            category=" network ",
            status=" OPEN ",
            priority=" HIGH ",
        )
        self.assertEqual([ticket["id"] for ticket in results], ["T001"])


if __name__ == "__main__":
    unittest.main()