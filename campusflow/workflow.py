
"""Manage ticket assignment, notes, status changes, and the open-ticket queue."""


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


def add_note(ticket_id, author, message, tickets):
    """Add a validated note to an unresolved ticket.

    Note IDs are generated separately for each ticket.
    Invalid notes do not consume a note ID.
    """
    if not isinstance(ticket_id, str) or not ticket_id.strip():
        raise ValueError("Ticket ID must be non-empty text.")

    ticket_id = ticket_id.strip()

    ticket = next(
        (
            item for item in tickets
            if isinstance(item, dict) and item.get("id") == ticket_id
        ),
        None,
    )

    if ticket is None:
        raise ValueError(f"Ticket {ticket_id} was not found.")

    if ticket.get("status") not in {"open", "in_progress"}:
        raise ValueError("Notes can only be added to unresolved tickets.")

    if not isinstance(author, str) or not author.strip():
        raise ValueError("Note author cannot be empty.")

    if not isinstance(message, str):
        raise ValueError("Note message must be text.")

    author = author.strip()
    message = message.strip()

    if not 5 <= len(message) <= 300:
        raise ValueError("Note message must contain 5 to 300 characters.")

    notes = ticket.get("notes", [])

    if not isinstance(notes, list):
        raise ValueError("Ticket notes must be stored as a list.")

    note_numbers = []

    for note in notes:
        if not isinstance(note, dict):
            raise ValueError("Existing notes must be valid note objects.")

        note_id = note.get("note_id", "")

        if (
            not isinstance(note_id, str)
            or len(note_id) < 2
            or not note_id.startswith("N")
            or not note_id[1:].isdigit()
        ):
            raise ValueError("Existing note has an invalid note ID.")

        note_numbers.append(int(note_id[1:]))

    next_number = max(note_numbers, default=0) + 1

    new_note = {
        "note_id": f"N{next_number:03d}",
        "author": author,
        "message": message,
    }

    # Change the ticket only after all validation succeeds.
    if "notes" not in ticket:
        ticket["notes"] = []

    ticket["notes"].append(new_note)

    return new_note


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
