"""Create and validate CampusFlow support tickets."""

CATEGORIES = {
    "network": "Network",
    "hardware": "Hardware",
    "software": "Software",
    "other": "Other",
}
URGENCIES = {"low", "medium", "high"}


def validate_title(title):
    """Validate and trim a ticket title."""
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Ticket title cannot be empty.")
    return title.strip()


def validate_category(category):
    """Validate and normalize a ticket category."""
    if not isinstance(category, str):
        raise ValueError(
            "Category must be Network, Hardware, Software, or Other."
        )
    normalized = category.strip().lower()
    if normalized not in CATEGORIES:
        raise ValueError(
            "Category must be Network, Hardware, Software, or Other."
        )
    return CATEGORIES[normalized]


def validate_urgency(urgency):
    """Validate and normalize urgency."""
    if not isinstance(urgency, str):
        raise ValueError("Urgency must be low, medium, or high.")
    normalized = urgency.strip().lower()
    if normalized not in URGENCIES:
        raise ValueError("Urgency must be low, medium, or high.")
    return normalized


def validate_affected_users(affected_users):
    """Require a positive integer, excluding booleans."""
    if (
        isinstance(affected_users, bool)
        or not isinstance(affected_users, int)
        or affected_users < 1
    ):
        raise ValueError("Affected users must be a positive integer.")
    return affected_users


def calculate_priority(urgency, affected_users):
    """Calculate ticket priority using the assessment rules."""
    urgency = validate_urgency(urgency)
    affected_users = validate_affected_users(affected_users)

    if urgency == "high" and affected_users >= 10:
        return "critical"
    if urgency == "high" or affected_users >= 10:
        return "high"
    if urgency == "medium" or affected_users >= 3:
        return "medium"
    return "low"


def generate_ticket_id(tickets):
    """Generate the next ticket ID after the largest valid T-number."""
    numbers = []
    for ticket in tickets:
        ticket_id = ticket.get("id", "")
        if isinstance(ticket_id, str) and ticket_id.startswith("T"):
            try:
                numbers.append(int(ticket_id[1:]))
            except ValueError:
                continue
    return f"T{max(numbers, default=0) + 1:03d}"


def create_ticket(tickets, title, category, urgency, affected_users):
    """Validate input and return a new ticket."""
    title = validate_title(title)
    category = validate_category(category)
    urgency = validate_urgency(urgency)
    affected_users = validate_affected_users(affected_users)

    return {
        "id": generate_ticket_id(tickets),
        "title": title,
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": calculate_priority(urgency, affected_users),
        "status": "open",
        "assigned_to": None,
    }
