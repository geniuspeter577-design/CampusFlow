"""Manage ticket assignment, status changes, and the open-ticket queue."""


def assign_ticket(ticket, assignee):
    """Assign a ticket to a named person."""
    if ticket["status"] == "resolved":
        raise ValueError(
            "Resolved tickets must be reopened before further changes."
        )

    if not isinstance(assignee, str):
        raise ValueError("Assignee name must be text.")

    assignee = assignee.strip()

    if not assignee:
        raise ValueError("Assignee name cannot be empty.")

    ticket["assigned_to"] = assignee
    return ticket


def update_ticket_status(ticket, new_status):
    """Validate and update a ticket's status."""
    if not isinstance(new_status, str):
        raise ValueError("Ticket status must be text.")

    new_status = new_status.strip().lower()
    allowed_statuses = {"open", "in_progress", "resolved"}

    if new_status not in allowed_statuses:
        raise ValueError("Invalid ticket status.")

    current_status = ticket["status"]

    if current_status == "resolved" and new_status != "open":
        raise ValueError(
            "Resolved tickets must be reopened before further changes."
        )

    if new_status == "in_progress" and not ticket["assigned_to"]:
        raise ValueError(
            "A ticket must be assigned before it can move to in_progress."
        )

    ticket["status"] = new_status
    return ticket


def get_open_ticket_queue(tickets):
    """Return open tickets ordered by priority, then numeric ticket ID."""
    priority_order = {
        "critical": 1,
        "high": 2,
        "medium": 3,
        "low": 4,
    }

    open_tickets = [
        ticket for ticket in tickets
        if ticket["status"] == "open"
    ]

    return sorted(
        open_tickets,
        key=lambda ticket: (
            priority_order[ticket["priority"]],
            int(ticket["id"][1:]),
        ),
    )
