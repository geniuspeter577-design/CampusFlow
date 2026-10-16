import unittest

from campusflow.search import search_tickets, sort_by_priority_then_id


def make(ticket_id, title, category, status, priority):
    return {
        "id": ticket_id, "title": title, "category": category,
        "status": status, "priority": priority, "assigned_to": None,
    }


class TestSearch(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            make("T001", "WI-FI is down", "Network", "open", "high"),
            make("T002", "wi-fi slow in lab", "Network", "resolved", "low"),
            make("T010", "Laptop wi-fi card broken", "Hardware", "open", "critical"),
            make("T002", "Printer jam", "Hardware", "open", "medium"),
        ]

    def test_title_ignores_case_and_matches_substring(self):
        ids = [t["title"] for t in search_tickets(self.tickets, title="wi-fi")]
        self.assertEqual(len(ids), 3)
        self.assertEqual(len(search_tickets(self.tickets, title="WI-FI")), 3)

    def test_filters_combine_with_and(self):
        results = search_tickets(
            self.tickets, title="wi-fi", category="network", status="open"
        )
        self.assertEqual([t["id"] for t in results], ["T001"])

    def test_empty_filters_return_everything(self):
        self.assertEqual(len(search_tickets(self.tickets)), 4)

    def test_invalid_filter_is_rejected(self):
        with self.assertRaises(ValueError):
            search_tickets(self.tickets, status="banana")
        with self.assertRaises(ValueError):
            search_tickets(self.tickets, category="Food")
        with self.assertRaises(ValueError):
            search_tickets(self.tickets, priority="urgent")

    def test_search_does_not_modify_tickets(self):
        before = [t.copy() for t in self.tickets]
        search_tickets(self.tickets, title="wi-fi", status="open")
        self.assertEqual(self.tickets, before)

    def test_sort_uses_numeric_id_not_text(self):
        tickets = [
            make("T10", "a", "Other", "open", "high"),
            make("T2", "b", "Other", "open", "high"),
        ]
        ordered = sort_by_priority_then_id(tickets)
        self.assertEqual([t["id"] for t in ordered], ["T2", "T10"])

    def test_sort_puts_critical_first(self):
        ordered = sort_by_priority_then_id(self.tickets)
        self.assertEqual(ordered[0]["priority"], "critical")


if __name__ == "__main__":
    unittest.main()
