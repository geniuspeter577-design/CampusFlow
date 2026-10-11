"""Create and validate CampusFlow support tickets."""

CATEGORIES = {"network": "Network", "hardware": "Hardware",
              "software": "Software", "other": "Other"}
URGENCIES = {"low", "medium", "high"}


def calculate_priority(urgency, affected_users):
    """Apply the assessment's priority rules."""
    if urgency == "high" and affected_users >= 10:
        return "critical"
    if urgency == "high" or affected_users >= 10:
        return "high"
    if urgency == "medium" or affected_users >= 3:
        return "medium"
    return "low"


def create_ticket(tickets, title, category, urgency, affected_users):
    """Validate input and return a new ticket with the next available ID."""
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Ticket title cannot be empty.")
    if not isinstance(category, str) or category.strip().lower() not in CATEGORIES:
        raise ValueError("Category must be Network, Hardware, Software, or Other.")
    if not isinstance(urgency, str) or urgency.strip().lower() not in URGENCIES:
        raise ValueError("Urgency must be low, medium, or high.")
    if (isinstance(affected_users, bool) or
            not isinstance(affected_users, int) or affected_users < 1):
        raise ValueError("Affected users must be a positive integer.")

    numbers = []
    for ticket in tickets:
        ticket_id = ticket.get("id", "")
        if isinstance(ticket_id, str) and ticket_id.startswith("T"):
            try:
                numbers.append(int(ticket_id[1:]))
            except ValueError:
                pass

    number = max(numbers, default=0) + 1
    normalized_urgency = urgency.strip().lower()
    ticket = {
        "id": f"T{number:03d}",
        "title": title.strip(),
        "category": CATEGORIES[category.strip().lower()],
        "urgency": normalized_urgency,
        "affected_users": affected_users,
        "priority": calculate_priority(normalized_urgency, affected_users),
        "status": "open",
        "assigned_to": None,
    }
    return ticket
