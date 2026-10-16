"""Structured follow-up notes: {note_id, author, message} per ticket."""

NOTE_MIN = 5
NOTE_MAX = 300
NOTE_STATUSES = ("open", "in_progress")


def next_note_id(ticket):
    """Next per-ticket note ID (N001, N002...). Ignores old plain-text notes."""
    numbers = []
    for note in ticket.get("notes", []):
        if isinstance(note, dict):
            note_id = note.get("note_id", "")
            if isinstance(note_id, str) and note_id.startswith("N"):
                try:
                    numbers.append(int(note_id[1:]))
                except ValueError:
                    continue
    return f"N{max(numbers, default=0) + 1:03d}"


def _find(tickets, ticket_id):
    if not isinstance(ticket_id, str):
        raise ValueError("Ticket ID must be text.")
    wanted = ticket_id.strip().upper()
    for ticket in tickets:
        if ticket.get("id", "").upper() == wanted:
            return ticket
    raise ValueError("Ticket not found.")


def add_note(tickets, ticket_id, author, message):
    """Add a note. Validates everything first; raises ValueError, changes nothing on failure."""
    ticket = _find(tickets, ticket_id)
    if ticket["status"] not in NOTE_STATUSES:
        raise ValueError("Notes can only be added to open or in_progress tickets.")
    if not isinstance(author, str) or not author.strip():
        raise ValueError("Note author cannot be empty.")
    if not isinstance(message, str):
        raise ValueError("Note message must be text.")
    message = message.strip()
    if not NOTE_MIN <= len(message) <= NOTE_MAX:
        raise ValueError(
            f"Note message must be {NOTE_MIN} to {NOTE_MAX} characters."
        )
    if not isinstance(ticket.get("notes", []), list):
        raise ValueError("Ticket notes must be stored as a list.")

    note = {
        "note_id": next_note_id(ticket),
        "author": author.strip(),
        "message": message,
    }
    ticket.setdefault("notes", []).append(note)
    return note


def get_notes(tickets, ticket_id):
    """Return a ticket's structured notes in note-ID order (read-only)."""
    ticket = _find(tickets, ticket_id)
    notes = [n for n in ticket.get("notes", []) if isinstance(n, dict)]
    return sorted(notes, key=lambda n: int(n["note_id"][1:]))
