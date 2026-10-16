"""Load and save tickets using JSON persistence."""

import json
from pathlib import Path


def load_tickets(path="tickets.json"):
    """Return saved tickets, or an empty list if the file does not exist."""
    file_path = Path(path)
    if not file_path.exists():
        return []
    try:
        with file_path.open("r", encoding="utf-8") as file:
            tickets = json.load(file)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError(f"Cannot read malformed ticket data from {file_path}.") from exc
    if not isinstance(tickets, list):
        raise ValueError(f"Ticket data in {file_path} must be a JSON list.")
    if any(not isinstance(ticket, dict) for ticket in tickets):
        raise ValueError(f"Ticket data in {file_path} contains an invalid record.")
    return tickets


def save_tickets(tickets, path="tickets.json"):
    """Persist tickets as readable JSON."""
    file_path = Path(path)
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=2, ensure_ascii=False)
        file.write("\n")


def load_validated_tickets(path="tickets.json"):
    """Load AND fully validate tickets. Raises ValueError if anything is wrong.

    Returns a new list only when everything is valid, so the caller's
    current tickets are never touched by a failed load.
    """
    from campusflow.validation import validate_ticket_collection

    return validate_ticket_collection(load_tickets(path))
