"""Generate summary reports for CampusFlow tickets."""

CATEGORY_NAMES = ("Network", "Hardware", "Software", "Other")


def generate_ticket_report(tickets):
    """Count tickets by status, priority and category. Read-only."""
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
    for name in CATEGORY_NAMES:
        report[name] = 0

    for ticket in tickets:
        report[ticket["status"]] += 1
        report[ticket["priority"]] += 1
        category = ticket.get("category")
        if category in CATEGORY_NAMES:
            report[category] += 1

    report["unresolved"] = report["open"] + report["in_progress"]
    if report["total"] == 0:
        report["resolution_percentage"] = 0.0
    else:
        report["resolution_percentage"] = round(
            report["resolved"] / report["total"] * 100, 1
        )
    return report
