import unittest

from campusflow.reports import generate_ticket_report


class TestTicketReport(unittest.TestCase):

    def test_report_counts_tickets_correctly(self):
        tickets = [
            {"id": "T001", "status": "open", "priority": "critical",
             "category": "Network"},
            {"id": "T002", "status": "open", "priority": "high",
             "category": "Network"},
            {"id": "T003", "status": "resolved", "priority": "medium",
             "category": "Software"},
            {"id": "T004", "status": "in_progress", "priority": "low",
             "category": "Hardware"},
        ]

        report = generate_ticket_report(tickets)

        self.assertEqual(report["total"], 4)
        self.assertEqual(report["open"], 2)
        self.assertEqual(report["in_progress"], 1)
        self.assertEqual(report["resolved"], 1)
        self.assertEqual(report["critical"], 1)
        self.assertEqual(report["high"], 1)
        self.assertEqual(report["medium"], 1)
        self.assertEqual(report["low"], 1)
        self.assertEqual(report["unresolved"], 3)
        self.assertEqual(report["resolution_percentage"], 25.0)
        self.assertEqual(report["categories"]["Network"], 2)

    def test_empty_ticket_list(self):
        report = generate_ticket_report([])

        self.assertEqual(report["total"], 0)
        self.assertEqual(report["unresolved"], 0)
        self.assertEqual(report["resolution_percentage"], 0)
        self.assertEqual(report["categories"], {})

    def test_report_does_not_modify_tickets(self):
        tickets = [
            {"id": "T001", "status": "open", "priority": "critical",
             "category": "Network"},
        ]
        original = [ticket.copy() for ticket in tickets]

        generate_ticket_report(tickets)

        self.assertEqual(tickets, original)

    def test_all_resolved_gives_100_percent(self):
        tickets = [
            {"id": "T001", "status": "resolved", "priority": "low",
             "category": "Other"},
        ]

        report = generate_ticket_report(tickets)

        self.assertEqual(report["resolution_percentage"], 100.0)
        self.assertEqual(report["unresolved"], 0)


if __name__ == "__main__":
    unittest.main()