import unittest

from campusflow.reports import generate_ticket_report


class TestTicketReport(unittest.TestCase):

    def test_report_counts_tickets_correctly(self):
        tickets = [
            {"id": "T001", "status": "open", "priority": "critical"},
            {"id": "T002", "status": "open", "priority": "high"},
            {"id": "T003", "status": "resolved", "priority": "medium"},
            {"id": "T004", "status": "in_progress", "priority": "low"},
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

    def test_empty_ticket_list(self):
        report = generate_ticket_report([])

        self.assertEqual(report["total"], 0)
        self.assertEqual(report["open"], 0)
        self.assertEqual(report["in_progress"], 0)
        self.assertEqual(report["resolved"], 0)
        self.assertEqual(report["critical"], 0)
        self.assertEqual(report["high"], 0)
        self.assertEqual(report["medium"], 0)
        self.assertEqual(report["low"], 0)


if __name__ == "__main__":
    unittest.main()

    def test_report_does_not_modify_tickets(self):
        tickets = [
            {"id": "T001", "status": "open", "priority": "critical"},
            {"id": "T002", "status": "resolved", "priority": "low"},
        ]
        original_tickets = [ticket.copy() for ticket in tickets]

        generate_ticket_report(tickets)

        self.assertEqual(tickets, original_tickets)

    def test_report_counts_multiple_tickets_in_same_category(self):
        tickets = [
            {"id": "T001", "status": "open", "priority": "high"},
            {"id": "T002", "status": "open", "priority": "high"},
            {"id": "T003", "status": "in_progress", "priority": "high"},
        ]

        report = generate_ticket_report(tickets)

        self.assertEqual(report["total"], 3)
        self.assertEqual(report["open"], 2)
        self.assertEqual(report["in_progress"], 1)
        self.assertEqual(report["high"], 3)
