"""Validate a whole ticket collection BEFORE it is trusted."""

import copy
import re

from campusflow.tickets import (
    CATEGORIES, URGENCIES, calculate_priority, validate_affected_users,
)

REQUIRED_KEYS = (
    "id", "title", "category", "urgency", "affected_users",
    "priority", "status", "assigned_to",
)
STATUSES = ("open", "in_progress", "resolved")
TICKET_ID = re.compile(r"^T\d+$")
NOTE_ID = re.compile(r"^N\d+$")


def _validate_notes(label, notes):
    if not isinstance(notes, list):
        raise ValueError(f"{label}: notes must be a list.")
    seen = set()
    for note in notes:
        if not isinstance(note, dict):
            raise ValueError(f"{label}: each note must be a dictionary.")
        for key in ("note_id", "author", "message"):
            if not isinstance(note.get(key), str):
                raise ValueError(f"{label}: note is missing text field '{key}'.")
        if not NOTE_ID.match(note["note_id"]):
            raise ValueError(f"{label}: bad note ID '{note['note_id']}'.")
        if not note["author"].strip():
            raise ValueError(f"{label}: note author cannot be empty.")
        if not 5 <= len(note["message"].strip()) <= 300:
            raise ValueError(f"{label}: note message must be 5 to 300 characters.")
        if note["note_id"] in seen:
            raise ValueError(f"{label}: duplicate note ID '{note['note_id']}'.")
        seen.add(note["note_id"])


def validate_ticket_collection(data):
    """Return a validated COPY of the tickets, or raise ValueError.

    The input is never changed. Old tickets with no 'notes' get an empty list.
    """
    if not isinstance(data, list):
        raise ValueError("Ticket data must be a list.")

    checked = []
    seen_ids = set()
    for index, record in enumerate(data, start=1):
        if not isinstance(record, dict):
            raise ValueError(f"Record {index} is not a dictionary.")
        for key in REQUIRED_KEYS:
            if key not in record:
                raise ValueError(f"Record {index} is missing '{key}'.")

        ticket = copy.deepcopy(record)
        ticket_id = ticket["id"]
        if not isinstance(ticket_id, str) or not TICKET_ID.match(ticket_id):
            raise ValueError(f"Record {index} has an invalid ID.")
        if ticket_id in seen_ids:
            raise ValueError(f"Duplicate ticket ID {ticket_id}.")
        seen_ids.add(ticket_id)

        label = f"Ticket {ticket_id}"
        if not isinstance(ticket["title"], str) or not ticket["title"].strip():
            raise ValueError(f"{label}: title cannot be empty.")
        if ticket["category"] not in CATEGORIES.values():
            raise ValueError(f"{label}: invalid category.")
        if ticket["urgency"] not in URGENCIES:
            raise ValueError(f"{label}: invalid urgency.")
        validate_affected_users(ticket["affected_users"])
        if ticket["priority"] != calculate_priority(
            ticket["urgency"], ticket["affected_users"]
        ):
            raise ValueError(f"{label}: priority does not match urgency and users.")
        if ticket["status"] not in STATUSES:
            raise ValueError(f"{label}: invalid status.")
        assignee = ticket["assigned_to"]
        if assignee is not None and (
            not isinstance(assignee, str) or not assignee.strip()
        ):
            raise ValueError(f"{label}: invalid assignee.")
        if ticket["status"] == "in_progress" and assignee is None:
            raise ValueError(f"{label}: in_progress tickets must be assigned.")

        ticket.setdefault("notes", [])
        _validate_notes(label, ticket["notes"])
        checked.append(ticket)
    return checked
