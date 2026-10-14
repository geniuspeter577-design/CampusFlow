import unittest
from campusflow.search import search_tickets


class TestTicketSearch(unittest.TestCase):
    def setUp(self):
        self.tickets = [
            {
                "id": "T001",
                "title": "Campus network is down",
                "category": "Network",
                "status": "open",
                "priority": "critical",
            },
            {
                "id": "T002",
                "title": "Broken computer in lab",
                "category": "Hardware",
                "status": "in_progress",
                "priority": "high",
            },
            {
                "id": "T003",
                "title": "Install office software",
                "category": "Software",
                "status": "resolved",
                "priority": "low",
            },
        ]

    def test_no_filters_returns_all_tickets(self):
        result = search_tickets(self.tickets)
        self.assertEqual(len(result), 3)

    def test_search_title_ignores_case(self):
        result = search_tickets(self.tickets, keyword="NETWORK")
        self.assertEqual([ticket["id"] for ticket in result], ["T001"])

    def test_filter_by_status(self):
        result = search_tickets(self.tickets, status="open")
        self.assertEqual([ticket["id"] for ticket in result], ["T001"])

    def test_filter_by_priority(self):
        result = search_tickets(self.tickets, priority="high")
        self.assertEqual([ticket["id"] for ticket in result], ["T002"])

    def test_combine_filters(self):
        result = search_tickets(
            self.tickets,
            keyword="computer",
            status="in_progress",
        )
        self.assertEqual([ticket["id"] for ticket in result], ["T002"])

    def test_no_match_returns_empty_list(self):
        result = search_tickets(self.tickets, keyword="printer")
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()