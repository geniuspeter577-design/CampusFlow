"""Generate summary reports for CampusFlow tickets."""


def generate_ticket_report(tickets):
    """Count tickets by status, priority, category, and resolution."""
    statuses = {"open": 0, "in_progress": 0, "resolved": 0}
    priorities = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    categories = {}

    for ticket in tickets:
        status = ticket["status"]
        priority = ticket["priority"]
        category = ticket.get("category", "Other")

        if status in statuses:
            statuses[status] += 1
        if priority in priorities:
            priorities[priority] += 1

        categories[category] = categories.get(category, 0) + 1

    total = len(tickets)
    resolved = statuses["resolved"]
    unresolved = statuses["open"] + statuses["in_progress"]

    report = {
        "total": total,
        **statuses,
        **priorities,
        "unresolved": unresolved,
        "resolution_percentage": (
            round((resolved / total) * 100, 2) if total else 0
        ),
        "categories": categories,
    }
    return report