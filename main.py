"""Command-line interface for CampusFlow."""

from campusflow.tickets import create_ticket
from campusflow.workflow import (
    assign_ticket,
    update_ticket_status,
    get_open_ticket_queue,
)
from campusflow.reports import generate_ticket_report
from campusflow.storage import load_tickets, save_tickets
from campusflow.search import search_tickets


def main():
    """Run the CampusFlow helpdesk menu."""
    tickets = load_tickets()

    while True:
        print("\nCampusFlow Helpdesk")
        print("1. Create ticket")
        print("2. List tickets")
        print("3. Assign ticket")
        print("4. Update ticket status")
        print("5. Show open queue")
        print("6. Show report")
        print("7. Search tickets")
        print("0. Save and exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                title = input("Title: ")
                category = input(
                    "Category (Network/Hardware/Software/Other): "
                )
                urgency = input("Urgency (low/medium/high): ")
                affected = int(input("Number of affected users: "))

                ticket = create_ticket(
                    tickets, title, category, urgency, affected
                )
                tickets.append(ticket)
                save_tickets(tickets)

                print(
                    f"Created {ticket['id']} "
                    f"with {ticket['priority']} priority."
                )

            elif choice == "2":
                if not tickets:
                    print("No tickets found.")

                for ticket in tickets:
                    print(
                        f"{ticket['id']} | {ticket['status']} | "
                        f"{ticket['priority']} | {ticket['title']}"
                    )

            elif choice == "3":
                ticket = _find_ticket(
                    tickets, input("Ticket ID: ")
                )

                if ticket:
                    assign_ticket(
                        ticket, input("Assignee name: ")
                    )
                    save_tickets(tickets)
                    print("Ticket assigned.")

            elif choice == "4":
                ticket = _find_ticket(
                    tickets, input("Ticket ID: ")
                )

                if ticket:
                    status = input(
                        "New status (open/in_progress/resolved): "
                    )
                    update_ticket_status(ticket, status)
                    save_tickets(tickets)
                    print("Ticket status updated.")

            elif choice == "5":
                queue = get_open_ticket_queue(tickets)

                if not queue:
                    print("No open tickets.")

                for ticket in queue:
                    print(
                        f"{ticket['id']} | {ticket['priority']} | "
                        f"{ticket['title']}"
                    )

            elif choice == "6":
                report = generate_ticket_report(tickets)

                for name, count in report.items():
                    print(f"{name}: {count}")

            elif choice == "7":
                keyword = input(
                    "Title keyword (press Enter to skip): "
                ).strip()

                status = input(
                    "Status (open/in_progress/resolved, "
                    "or Enter to skip): "
                ).strip()

                priority = input(
                    "Priority (critical/high/medium/low, "
                    "or Enter to skip): "
                ).strip()

                results = search_tickets(
                    tickets,
                    keyword=keyword or None,
                    status=status or None,
                    priority=priority or None,
                )

                if not results:
                    print("No matching tickets found.")
                else:
                    print("\nMatching tickets:")

                    for ticket in results:
                        print(
                            f"{ticket['id']} | {ticket['status']} | "
                            f"{ticket['priority']} | {ticket['title']}"
                        )

            elif choice == "0":
                save_tickets(tickets)
                print("Tickets saved. Goodbye.")
                break

            else:
                print(
                    "Invalid option. "
                    "Choose one of the displayed options."
                )

        except (ValueError, KeyError) as exc:
            print(f"Error: {exc}")


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