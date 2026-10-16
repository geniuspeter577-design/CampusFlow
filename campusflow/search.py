"""Read-only ticket search. Never changes the tickets it receives."""

from campusflow.tickets import CATEGORIES

STATUSES = ("open", "in_progress", "resolved")
PRIORITY_ORDER = {"critical": 1, "high": 2, "medium": 3, "low": 4}


def _clean(value):
    """Turn None or whitespace into an empty string."""
    if value is None:
        return ""
    if not isinstance(value, str):
        raise ValueError("Search filters must be text.")
    return value.strip()


def search_tickets(tickets, title="", category="", status="", priority=""):
    """Return tickets matching ALL supplied filters. Empty means no filter."""
    title = _clean(title).casefold()
    category = _clean(category).casefold()
    status = _clean(status).casefold()
    priority = _clean(priority).casefold()

    if category and category not in CATEGORIES:
        raise ValueError("Category must be Network, Hardware, Software, or Other.")
    if status and status not in STATUSES:
        raise ValueError("Status must be open, in_progress, or resolved.")
    if priority and priority not in PRIORITY_ORDER:
        raise ValueError("Priority must be critical, high, medium, or low.")

    results = []
    for ticket in tickets:
        if title and title not in ticket["title"].casefold():
            continue
        if category and ticket["category"].casefold() != category:
            continue
        if status and ticket["status"] != status:
            continue
        if priority and ticket["priority"] != priority:
            continue
        results.append(ticket)
    return results


def sort_by_priority_then_id(tickets):
    """Return a new list sorted by priority, then numeric ticket ID."""
    return sorted(
        tickets,
        key=lambda t: (PRIORITY_ORDER[t["priority"]], int(t["id"][1:])),
    )
