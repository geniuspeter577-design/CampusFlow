"""Generate summary reports for CampusFlow tickets."""


def generate_ticket_report(tickets):
    """Count tickets by status and priority."""
    report = {
        "total": len(tickets),
        "open": 0,
        "in_progress": 0,
        "resolved": 0,
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
    }

    for ticket in tickets:
        report[ticket["status"]] += 1
        report[ticket["priority"]] += 1

    return report
