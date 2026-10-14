"""Search and filter CampusFlow support tickets."""


def search_tickets(tickets, keyword=None, status=None, priority=None):
    """Search tickets by title, status, and priority."""

    results = []

    for ticket in tickets:
        # Search the title if a keyword was provided.
        if keyword is not None:
            if keyword.strip().lower() not in ticket["title"].lower():
                continue

        # Filter by status if one was provided.
        if status is not None:
            if ticket["status"].lower() != status.strip().lower():
                continue

        # Filter by priority if one was provided.
        if priority is not None:
            if ticket["priority"].lower() != priority.strip().lower():
                continue

        results.append(ticket)

    return results