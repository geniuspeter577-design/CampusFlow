"""CampusFlow command-line interface."""

from campusflow.tickets import (
    create_ticket,
    validate_category,
    validate_urgency,
    validate_affected_users,
)
from campusflow.workflow import (
    assign_ticket,
    update_ticket_status,
    get_open_ticket_queue,
    add_note,
)
from campusflow.search import search_tickets
from campusflow.reports import generate_ticket_report
from campusflow.storage import load_tickets, save_tickets


def find_ticket(tickets, ticket_id):
    for ticket in tickets:
        if str(ticket.get("id")) == str(ticket_id):
            return ticket
    return None


def display_tickets(tickets):
    if not tickets:
        print("\nNo tickets found.")
        return

    for ticket in tickets:
        print(
            f"ID: {ticket['id']} | Title: {ticket['title']} | "
            f"Category: {ticket['category']} | "
            f"Priority: {ticket['priority']} | "
            f"Status: {ticket['status']} | "
            f"Assignee: {ticket.get('assigned_to') or 'Unassigned'}"
        )


def create_new_ticket(tickets):
    title = input("Title: ").strip()
    category = input("Category: ").strip()
    urgency = input("Urgency: ").strip()

    try:
        affected_users = int(input("Affected users: ").strip())
        validate_category(category)
        validate_urgency(urgency)
        validate_affected_users(affected_users)

        ticket = create_ticket(
            tickets, title, category, urgency, affected_users
        )
        save_tickets(tickets)
        print(f"Ticket created. ID: {ticket['id']}")
    except (ValueError, TypeError) as error:
        print(f"Could not create ticket: {error}")


def assign_existing_ticket(tickets):
    ticket = find_ticket(tickets, input("Ticket ID: ").strip())
    if ticket is None:
        print("Ticket not found.")
        return

    assignee = input("Assignee: ").strip()
    try:
        assign_ticket(ticket, assignee)
        save_tickets(tickets)
        print("Ticket assigned successfully.")
    except (ValueError, TypeError) as error:
        print(f"Could not assign ticket: {error}")


def change_ticket_status(tickets):
    ticket = find_ticket(tickets, input("Ticket ID: ").strip())
    if ticket is None:
        print("Ticket not found.")
        return

    status = input("New status (open/in_progress/resolved): ").strip()
    try:
        update_ticket_status(ticket, status)
        save_tickets(tickets)
        print("Status updated successfully.")
    except (ValueError, TypeError) as error:
        print(f"Could not update status: {error}")


def add_ticket_note(tickets):
    ticket_id = input("Ticket ID: ").strip()
    if find_ticket(tickets, ticket_id) is None:
        print("Ticket not found.")
        return

    author = input("Your name: ").strip()
    message = input("Note: ").strip()

    try:
        add_note(ticket_id, author, message, tickets)
        save_tickets(tickets)
        print("Note added successfully.")
    except (ValueError, TypeError) as error:
        print(f"Could not add note: {error}")


def show_ticket_details(tickets):
    ticket = find_ticket(tickets, input("Ticket ID: ").strip())
    if ticket is None:
        print("Ticket not found.")
        return

    for key, value in ticket.items():
        if key != "notes":
            print(f"{key.replace('_', ' ').title()}: {value}")

    print("\nNotes:")
    for note in ticket.get("notes", []):
        print(
            f"{note.get('note_id')} | {note.get('author')} | "
            f"{note.get('message')}"
        )
    if not ticket.get("notes"):
        print("No notes yet.")


def search_and_filter(tickets):
    title = input("Title filter (Enter to skip): ").strip()
    category = input("Category filter (Enter to skip): ").strip()
    status = input("Status filter (Enter to skip): ").strip()
    priority = input("Priority filter (Enter to skip): ").strip()

    results = search_tickets(
        tickets,
        title=title,
        category=category,
        status=status,
        priority=priority,
    )
    display_tickets(results)
    print(f"Matching tickets: {len(results)}")


def show_report(tickets):
    report = generate_ticket_report(tickets)

    print("\nCampusFlow Ticket Report")
    print("=" * 30)
    print(f"Total: {report['total']}")
    print(f"Open: {report['open']}")
    print(f"In progress: {report['in_progress']}")
    print(f"Resolved: {report['resolved']}")
    print(f"Unresolved: {report['unresolved']}")
    print(f"Resolution: {report['resolution_percentage']}%")

    print("\nPriorities:")
    for priority in ("critical", "high", "medium", "low"):
        print(f"{priority.title()}: {report[priority]}")

    print("\nCategories:")
    if report["categories"]:
        for category, count in report["categories"].items():
            print(f"{category}: {count}")
    else:
        print("No tickets by category yet.")


def main():
    try:
        tickets = load_tickets()
    except (OSError, ValueError, TypeError) as error:
        print(f"Could not load tickets: {error}")
        return

    while True:
        print(
            "\n========== CampusFlow ==========\n"
            "1. Create ticket\n"
            "2. List tickets\n"
            "3. Assign ticket\n"
            "4. Update status\n"
            "5. Open ticket queue\n"
            "6. Add ticket note\n"
            "7. Ticket details\n"
            "8. Search and filter\n"
            "9. Generate report\n"
            "0. Exit"
        )

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                create_new_ticket(tickets)
            elif choice == "2":
                display_tickets(tickets)
            elif choice == "3":
                assign_existing_ticket(tickets)
            elif choice == "4":
                change_ticket_status(tickets)
            elif choice == "5":
                display_tickets(get_open_ticket_queue(tickets))
            elif choice == "6":
                add_ticket_note(tickets)
            elif choice == "7":
                show_ticket_details(tickets)
            elif choice == "8":
                search_and_filter(tickets)
            elif choice == "9":
                show_report(tickets)
            elif choice == "0":
                print("Exiting CampusFlow.")
                break
            else:
                print("Invalid option. Choose 0 to 9.")
        except (ValueError, TypeError, KeyError) as error:
            print(f"Operation failed: {error}")


if __name__ == "__main__":
    main()
