"""Search and filter CampusFlow tickets."""


def search_tickets(
    tickets,
    title="",
    category="",
    status="",
    priority="",
):
    """Return tickets matching all supplied filters without modifying input."""
    title = title.strip().casefold() if isinstance(title, str) else ""
    category = category.strip().casefold() if isinstance(category, str) else ""
    status = status.strip().casefold() if isinstance(status, str) else ""
    priority = priority.strip().casefold() if isinstance(priority, str) else ""

    results = []

    for ticket in tickets:
        if title and title not in ticket.get("title", "").casefold():
            continue
        if category and category != ticket.get("category", "").casefold():
            continue
        if status and status != ticket.get("status", "").casefold():
            continue
        if priority and priority != ticket.get("priority", "").casefold():
            continue

        results.append(ticket)

    return results