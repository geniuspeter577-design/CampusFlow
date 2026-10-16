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

    def test_empty_ticket_list_has_zero_percent(self):
        report = generate_ticket_report([])
        self.assertEqual(report["total"], 0)
        self.assertEqual(report["unresolved"], 0)
        self.assertEqual(report["resolution_percentage"], 0.0)

    def test_report_does_not_modify_tickets(self):
        tickets = [
            {"id": "T001", "status": "open", "priority": "critical"},
            {"id": "T002", "status": "resolved", "priority": "low"},
        ]
        original = [ticket.copy() for ticket in tickets]
        generate_ticket_report(tickets)
        self.assertEqual(tickets, original)

    def test_report_counts_multiple_tickets_in_same_priority(self):
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

    def test_unresolved_and_resolution_percentage(self):
        tickets = [
            {"id": "T001", "status": "open", "priority": "low"},
            {"id": "T002", "status": "in_progress", "priority": "low"},
            {"id": "T003", "status": "open", "priority": "low"},
            {"id": "T004", "status": "resolved", "priority": "low"},
        ]
        report = generate_ticket_report(tickets)
        self.assertEqual(report["unresolved"], 3)
        self.assertEqual(report["resolved"], 1)
        self.assertEqual(report["resolution_percentage"], 25.0)

    def test_counts_by_category(self):
        tickets = [
            {"id": "T001", "status": "open", "priority": "low", "category": "Network"},
            {"id": "T002", "status": "open", "priority": "low", "category": "Network"},
            {"id": "T003", "status": "resolved", "priority": "low", "category": "Hardware"},
        ]
        report = generate_ticket_report(tickets)
        self.assertEqual(report["Network"], 2)
        self.assertEqual(report["Hardware"], 1)
        self.assertEqual(report["Software"], 0)
        self.assertEqual(report["Other"], 0)


if __name__ == "__main__":
    unittest.main()
