"""Command-line interface for CampusFlow Next."""

from campusflow.tickets import create_ticket
from campusflow.workflow import (
    assign_ticket, update_ticket_status, get_open_ticket_queue
)
from campusflow.reports import generate_ticket_report
from campusflow.storage import load_validated_tickets, save_tickets
from campusflow.notes import add_note, get_notes
from campusflow.search import search_tickets, sort_by_priority_then_id
from campusflow.cli import ask_valid, format_ticket_row

MENU = """
CampusFlow Helpdesk
1. Create ticket
2. List tickets
3. Assign ticket
4. Update ticket status
5. Show open queue
6. Show report
7. Add follow-up note
8. View ticket notes
9. Search tickets
10. Search tickets (sorted by priority)
0. Save and exit"""


def main():
    try:
        tickets = load_validated_tickets()
    except ValueError as exc:
        print(f"Cannot load tickets.json: {exc}")
        print("Fix or move that file, then start again. Nothing was changed.")
        return

    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                title = input("Title: ")
                category = input("Category (Network/Hardware/Software/Other): ")
                urgency = input("Urgency (low/medium/high): ")
                try:
                    affected = int(input("Number of affected users: "))
                except ValueError:
                    raise ValueError("Affected users must be a whole number.")
                ticket = create_ticket(tickets, title, category, urgency, affected)
                tickets.append(ticket)
                save_tickets(tickets)
                print(f"Created {ticket['id']} with {ticket['priority']} priority.")

            elif choice == "2":
                if not tickets:
                    print("No tickets found.")
                for ticket in tickets:
                    print(f"{ticket['id']} | {ticket['status']} | "
                          f"{ticket['priority']} | {ticket['title']}")

            elif choice == "3":
                ticket = _find_ticket(tickets, input("Ticket ID: "))
                if ticket:
                    assign_ticket(ticket, input("Assignee name: "))
                    save_tickets(tickets)
                    print("Ticket assigned.")

            elif choice == "4":
                ticket = _find_ticket(tickets, input("Ticket ID: "))
                if ticket:
                    status = input("New status (open/in_progress/resolved): ")
                    update_ticket_status(ticket, status)
                    save_tickets(tickets)
                    print("Ticket status updated.")

            elif choice == "5":
                queue = get_open_ticket_queue(tickets)
                if not queue:
                    print("No open tickets.")
                for ticket in queue:
                    print(f"{ticket['id']} | {ticket['priority']} | {ticket['title']}")

            elif choice == "6":
                _print_report(generate_ticket_report(tickets))

            elif choice == "7":
                ticket_id = input("Ticket ID: ")
                author = input("Your name: ")
                message = input("Note (5-300 characters): ")
                note = add_note(tickets, ticket_id, author, message)
                save_tickets(tickets)
                print(f"Note {note['note_id']} added.")

            elif choice == "8":
                notes = get_notes(tickets, input("Ticket ID: "))
                if not notes:
                    print("No notes for this ticket.")
                for note in notes:
                    print(f"{note['note_id']} | {note['author']} | {note['message']}")

            elif choice in ("9", "10"):
                _run_search(tickets, sort_by_priority=(choice == "10"))

            elif choice == "0":
                save_tickets(tickets)
                print("Tickets saved. Goodbye.")
                break

            else:
                print("Invalid option. Choose one of the displayed options.")

        except (ValueError, KeyError) as exc:
            print(f"Error: {exc}")


def _run_search(tickets, sort_by_priority=False):
    """Ask for filters (re-asking on bad input) and show matching tickets."""
    title = input("Title contains (Enter to skip): ")
    category = ask_valid(
        "Category (network/hardware/software/other, Enter to skip): ",
        ("", "network", "hardware", "software", "other"))
    status = ask_valid(
        "Status (open/in_progress/resolved, Enter to skip): ",
        ("", "open", "in_progress", "resolved"))
    priority = ask_valid(
        "Priority (critical/high/medium/low, Enter to skip): ",
        ("", "critical", "high", "medium", "low"))
    results = search_tickets(tickets, title, category, status, priority)
    if sort_by_priority:
        results = sort_by_priority_then_id(results)
    if not results:
        print("No matching tickets.")
    for ticket in results:
        print(format_ticket_row(ticket))


def _print_report(report):
    print(f"Total tickets: {report['total']}")
    print(f"Unresolved: {report['unresolved']} | Resolved: {report['resolved']}")
    print(f"Resolution: {report['resolution_percentage']}%")
    for group in (("open", "in_progress", "resolved"),
                  ("critical", "high", "medium", "low"),
                  ("Network", "Hardware", "Software", "Other")):
        print(" | ".join(f"{name}: {report[name]}" for name in group))


def _find_ticket(tickets, ticket_id):
    """Find a ticket by ID, ignoring surrounding whitespace and case."""
    ticket_id = ticket_id.strip().upper()
    for ticket in tickets:
        if ticket.get("id", "").upper() == ticket_id:
            return ticket
    print("Ticket not found.")
    return None


if __name__ == "__main__":
    main()
